import asyncio
from typing import Any

import pyaudiowpatch as pyaudio
import websockets
from pyaudiowpatch import Stream

from voice.config.config import Config


class AudioStreamer:
    """
    Audio streamer for streaming system and microphone audio to a WebSocket server.
    """

    def __init__(self, cfg: Config):
        """
        Initialize the AudioStreamer.

        Args:
            cfg (Config): Configuration object containing settings.
        """
        self.cfg = cfg

        self.running = False
        self.sending = False

    def _get_sys_info(self) -> dict[str, Any]:
        """
        Get the system device info.

        Returns:
            dict[str, Any]: System audio device info.
        """
        self.mode = RecognitionMode.CUSTOMER
        return self.p.get_default_wasapi_loopback()

    def _get_mic_info(self) -> dict[str, Any]:
        """
        Get the microphone device info.

        Returns:
            dict[str, Any]: Microphone audio device info.
        """
        self.mode = RecognitionMode.ADVISOR
        return self.p.get_default_input_device_info()

    # TODO: Skal nok laves forskellige efter om det er sys/mic
    def _create_stream(self, device_info: dict[str, Any]) -> Stream:
        """
        Create a stream for an audio device.

        Args:
            device_info (dict[str, Any]): Audio device info.

        Returns:
            Stream: Stream for the audio device.
        """
        if self.mode is RecognitionMode.CUSTOMER:
            return self.p.open(
                format=self.cfg.AUDIO_FORMAT,
                channels=device_info["maxInputChannels"],
                rate=int(device_info["defaultSampleRate"]),
                input=True,
                frames_per_buffer=self.cfg.AUDIO_FRAMES_PER_BUFFER,
                input_device_index=device_info["index"],
            )
        elif self.mode is RecognitionMode.ADVISOR:
            return self.p.open(
                format=self.cfg.AUDIO_FORMAT,
                channels=device_info["maxInputChannels"],
                rate=int(device_info["defaultSampleRate"]),
                input=True,
                frames_per_buffer=self.cfg.AUDIO_FRAMES_PER_BUFFER,
                input_device_index=device_info["index"],
            )

    def _create_sys_stream(self) -> None:
        """
        Create a stream for the system audio.
        """
        sys_info = self._get_sys_info()
        self.sys_name = sys_info["name"]
        self.stream_sys = self._create_stream(sys_info)

    def _create_mic_stream(self) -> None:
        """
        Create a stream for the microphone audio.
        """
        mic_info = self._get_sys_info()
        self.mic_name = mic_info["name"]
        self.stream_mic = self._create_stream(mic_info)

    async def _stream_audio(self, stream: Stream, url: str) -> None:
        """
        Stream audio to the WebSocket server.

        Args:
            stream (Stream): Stream for recieving audio.
            url (str): WebSocket server URL.
        """
        async with websockets.connect(url) as websocket:
            while self.running:
                if self.sending:
                    data = await asyncio.to_thread(
                        stream.read, self.cfg.AUDIO_FRAMES_PER_BUFFER
                    )
                    await websocket.send(data)
                else:
                    await asyncio.sleep(
                        self.cfg.SLEEP_DAY_SECONDS
                    )  # Prevent high CPU usage

    def _initialize(self) -> None:
        """
        Initialize the audio streamer.
        """
        self.group = asyncio.TaskGroup()
        self.p = pyaudio.PyAudio()
        self._create_sys_stream()
        self._create_mic_stream()

    async def start(self) -> None:
        """
        Start running the audio streamer.
        """
        self._initialize()
        await self.group.__aenter__()
        self.group.create_task(self._stream_audio(self.stream_sys, self.cfg.SYS_URL))
        self.group.create_task(self._stream_audio(self.stream_mic, self.cfg.MIC_URL))
        self.running = True

    def start_stream(self) -> None:
        """
        Start sending audio to the WebSocket server.
        """
        self.sending = True

    def pause_stream(self) -> None:
        """
        Pause sending audio to the WebSocket server.
        """
        self.sending = False

    async def stop(self) -> None:
        """
        Stop the audio streamer.
        """
        self.sending = False
        self.running = False
        await self._cleanup()

    async def _cleanup(self) -> None:
        """
        Clean up resources.
        """
        group = getattr(self, "group", None)
        if group is not None:
            for task in list(group._tasks):
                task.cancle()
            await group.__aexit__(None, None, None)

        for stream_attr in ("stream_sys", "stream_mic"):
            stream = getattr(self, stream_attr, None)
            if stream is not None:
                stream.stop_stream()
                stream.close()

        p = getattr(self, "p", None)
        if p is not None:
            p.terminate()
        if p is not None:
            p.terminate()
