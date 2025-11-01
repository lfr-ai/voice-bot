import asyncio
from asyncio import StreamReader, StreamWriter
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from voice.config.config import Config
from voice.managers.queue_manager import QueueManager
from voice.models.audio_streamer.audio_streamer_controller import (
    AudioStreamerController,
)
from voice.models.transcriber.transcriber import FasterWhisperSTT
from voice.utils.logger import Logger

cfg = Config()
logger = Logger.create(__name__, cfg.LOGS_DIR_PATH / "Backend.log")


async def _audio_receiver(reader: StreamReader, writer: StreamWriter, queue_name: str):
    """Handler for incoming audio data. Reads raw bytes and feeds STT queue."""
    try:
        while True:
            data = await reader.read(
                cfg.AUDIO_FRAMES_PER_BUFFER * 2 * getattr(cfg, "AUDIO_CHANNELS", 2)
            )
            if not data:
                break
            await app.state.stt.accept_bytes(queue_name, data)
    except Exception as e:
        print(f"[AudioReceiver:{queue_name}] Exception: {e}")
    finally:
        writer.close()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan handler: start STT, audio servers, and subprocess on startup; clean up on shutdown."""
    app.state.queue_manager = QueueManager()
    app.state.controller = AudioStreamerController(cfg)
    app.state.stt = FasterWhisperSTT(
        cfg=cfg,
        model_name="small",
        batch_seconds=5,
        on_transcript=lambda transcript: print(
            f"[{transcript.stream_name}] {transcript.text}"
        ),
    )

    # Ensure STT queues for system and mic
    await app.state.stt.ensure_queue("sys-queue")
    await app.state.stt.ensure_queue("mic-queue")
    await app.state.stt.start()

    # Start local servers to receive audio from subprocess
    host = cfg.HOST
    # Use command port +1/+2 for audio streams
    sys_port = cfg.AUDIO_STREAMER_TCP_PORT + 1
    mic_port = cfg.AUDIO_STREAMER_TCP_PORT + 2
    app.state.sys_server = await asyncio.start_server(
        lambda r, w: _audio_receiver(r, w, "sys-queue"), host, sys_port
    )
    app.state.mic_server = await asyncio.start_server(
        lambda r, w: _audio_receiver(r, w, "mic-queue"), host, mic_port
    )
    print(
        f"Audio servers listening on {host}:{sys_port} (sys) and {host}:{mic_port} (mic)"
    )

    # Start audio streamer subprocess after audio servers are listening
    await app.state.controller.start()

    yield

    # Shutdown: stop subprocess and STT, then close audio servers
    await app.state.controller.stop()
    await app.state.stt.stop()

    # Close servers
    app.state.sys_server.close()
    await app.state.sys_server.wait_closed()


app = FastAPI(lifespan=lifespan)


@app.post("/start_stream")
async def start_stream():
    """Start audio streaming."""
    await app.state.controller.device_check()
    await app.state.controller.send_command("start_stream")


@app.post("/pause_stream")
async def pause_stream():
    """Pause audio streaming."""
    await app.state.controller.send_command("pause_stream")


def main():
    uvicorn.run(app, host=cfg.HOST, port=cfg.PORT)


if __name__ == "__main__":
    main()
