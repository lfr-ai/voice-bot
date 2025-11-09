import asyncio
import os
import tempfile
import wave
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

import numpy as np
from faster_whisper import WhisperModel

from voice.config.config import Config
from voice.utils.logger import Logger

cfg = Config()
logger = Logger.create(__name__, cfg.LOGS_DIR_PATH / "stt.logs")


@dataclass
class Transcript:
    stream_name: str
    text: str
    segments: Any  # raw segments returned by faster-whisper (list/generator)
    info: Any


class FasterWhisperSTT:
    """
    A pseudo-live STT component that batches incoming raw PCM audio bytes and
    runs faster-whisper every `batch_seconds`, with Danish language transcription.
    """

    def __init__(
        self,
        cfg: Config,
        model_name: str = "small",
        device: Optional[str] = None,
        compute_type: Optional[str] = None,
        batch_seconds: float = 5.0,
        sample_rate: Optional[int] = None,
        channels: Optional[int] = None,
        language: str = "da",
        on_transcript: Optional[Callable[[Transcript], Any]] = None,
        output_queue: Optional[asyncio.Queue] = None,
    ):
        self.cfg = cfg
        self.model_name = model_name
        self.device = device or getattr(cfg, "STT_DEVICE", "cpu")
        self.compute_type = compute_type or getattr(cfg, "STT_COMPUTE_TYPE", None)
        self.batch_seconds = float(batch_seconds)
        self.sample_rate = (
            sample_rate
            or getattr(cfg, "AUDIO_SAMPLE_RATE", None)
            or getattr(cfg, "SAMPLE_RATE", None)
            or 48000
        )
        self.channels = channels or getattr(cfg, "AUDIO_CHANNELS", None) or 2
        self.language = language
        self.on_transcript = on_transcript
        self.output_queue = output_queue

        # internal structures
        self._queues: Dict[str, asyncio.Queue] = {}
        self._tasks: Dict[str, asyncio.Task] = {}
        self._model = None
        self._running = False
        self._model_lock = asyncio.Lock()

    async def start(self) -> None:
        """
        Load the faster-whisper model (lazy load) and start processing.
        """
        if WhisperModel is None:
            raise RuntimeError(
                "faster-whisper is not installed or failed to import. Install `faster-whisper`."
            )

        async with self._model_lock:
            if self._model is None:
                compute_type = self.compute_type
                if compute_type is None and self.device == "cpu":
                    compute_type = "int8"
                logger.info(
                    f"Loading faster-whisper model '{self.model_name}' device={self.device} compute_type={compute_type}"
                )
                try:
                    self._model = WhisperModel(
                        self.model_name, device=self.device, compute_type=compute_type
                    )
                except Exception:
                    logger.exception(
                        "Failed to load model with requested compute_type; trying default"
                    )
                    self._model = WhisperModel(self.model_name, device=self.device)

        self._running = True
        # start workers for already-registered queues
        for qn in list(self._queues.keys()):
            await self._ensure_task(qn)
        logger.info("FasterWhisperSTT started")

    async def stop(self) -> None:
        """
        Stop all workers and free model.
        """
        self._running = False
        # cancel tasks
        tasks = list(self._tasks.values())
        for t in tasks:
            t.cancel()
        # await cancellation
        await asyncio.gather(*tasks, return_exceptions=True)
        self._tasks.clear()
        # free model if present
        async with self._model_lock:
            self._model = None
        logger.info("FasterWhisperSTT stopped")

    async def ensure_queue(self, queue_name: str) -> None:
        """
        Create an input queue for a stream name and start its worker.
        """
        if queue_name in self._queues:
            return
        self._queues[queue_name] = asyncio.Queue()
        await self._ensure_task(queue_name)

    async def _ensure_task(self, queue_name: str) -> None:
        if not self._running:
            return
        if queue_name in self._tasks:
            # already running
            return
        task = asyncio.create_task(
            self._worker(queue_name), name=f"stt-worker-{queue_name}"
        )
        self._tasks[queue_name] = task

    async def accept_bytes(self, queue_name: str, data: bytes) -> None:
        """
        Accept bytes (raw PCM frames) from other sender and queue them.
        """
        if queue_name not in self._queues:
            # register automatically (no effect if already added)
            await self.ensure_queue(queue_name)

        # Put bytes into queue
        await self._queues[queue_name].put(data)

    async def _worker(self, queue_name: str) -> None:
        """
        Worker that drains an input queue every batch_seconds and transcribes it.
        """
        logger.info(f"STT worker started for queue: {queue_name}")
        q = self._queues[queue_name]
        try:
            while self._running:
                await asyncio.sleep(self.batch_seconds)
                # drain queue
                chunks = []
                while not q.empty():
                    try:
                        chunks.append(q.get_nowait())
                    except asyncio.QueueEmpty:
                        break
                if not chunks:
                    # nothing accumulated this interval
                    continue

                raw = b"".join(chunks)
                if len(raw) < 1024:
                    logger.debug(
                        f"STT {queue_name}: batch too small ({len(raw)} bytes) -> skipping"
                    )
                    continue

                # Write raw bytes to a temporary WAV file (mono).
                temp_path = await asyncio.to_thread(
                    self._raw_pcm_bytes_to_wav_file,
                    raw,
                    self.sample_rate,
                    self.channels,
                )

                # Ensure model loaded
                if self._model is None:
                    await self.start()

                # transcribe using faster-whisper with Danish language
                try:
                    segments, info = await asyncio.to_thread(
                        self._model.transcribe, temp_path, language=self.language
                    )
                    segs = list(segments) if hasattr(segments, "__iter__") else segments
                    text = "".join([getattr(s, "text", str(s)) for s in segs])
                except Exception as ex:
                    logger.exception(f"Transcription failed for {queue_name}: {ex}")
                    segs = []
                    info = None
                    text = ""
                finally:
                    # cleanup temp file
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass

                transcript = Transcript(
                    stream_name=queue_name, text=text, segments=segs, info=info
                )

                # call callback if provided
                if self.on_transcript:
                    try:
                        maybe = self.on_transcript(transcript)
                        if asyncio.iscoroutine(maybe):
                            await maybe
                    except Exception:
                        logger.exception("on_transcript callback raised")

                # push to output queue if provided
                if self.output_queue:
                    try:
                        await self.output_queue.put(transcript)
                    except Exception:
                        logger.exception("Failed to put transcript into output_queue")

                # also log short summary
                logger.info(
                    f"STT {queue_name}: transcribed {len(raw)} bytes -> '{text[:120]}'"
                )

        except asyncio.CancelledError:
            logger.info(f"STT worker cancelled for queue {queue_name}")
        except Exception:
            logger.exception(f"Unhandled exception in STT worker for {queue_name}")
        finally:
            if queue_name in self._tasks:
                self._tasks.pop(queue_name, None)
            logger.info(f"STT worker stopped for queue: {queue_name}")

    @staticmethod
    def _raw_pcm_bytes_to_wav_file(
        raw_bytes: bytes, sample_rate: int, channels: int
    ) -> str:
        """
        Convert raw PCM16LE bytes to a temporary mono WAV file path.
        """
        arr = np.frombuffer(raw_bytes, dtype=np.int16)
        if channels > 1:
            n_frames = arr.shape[0] // channels
            arr = arr[: n_frames * channels]
            arr = arr.reshape(-1, channels)
            mono = arr.astype(np.int32).mean(axis=1).astype(np.int16)
        else:
            mono = arr

        tf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tf_name = tf.name
        tf.close()

        with wave.open(tf_name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # int16
            wf.setframerate(int(sample_rate))
            wf.writeframes(mono.tobytes())

        return tf_name
