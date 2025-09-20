import asyncio
import json
import subprocess
import sys
from asyncio import TimeoutError
from asyncio.subprocess import Process

from voice.config.config import Config


class AudioStreamerController:
    """
    Controller for running and interacting with the audio streamer.
    """

    def __init__(self, cfg: Config):
        """
        Initialize the AudioStreamerController.

        Args:
            cfg (Config): Configuration object containing settings.
        """
        self.cfg = cfg

    async def _launch_subprocess(self) -> Process:
        """
        Launch the audio streamer and TCP server as a subprocess.

        Returns:
            Process: Subprocess for the audio streamer and TCP server.
        """
        return await asyncio.create_subprocess_exec(
            sys.executable, "-m", self.cfg.AUDIO_STREAMER_TCP_SERVER_MODULE_PATH
        )

    async def _get_device_names(self) -> dict[str, str]:
        """
        Get the names of the system and microphone audio devices.

        Returns:
            dict[str, str]: The device names.
        """
        code = (
            "import json\n"
            "import pyaudiowpatch as pyaudio\n"
            "pa = pyaudio.Pyaudio()\n"
            "sys_name = pa.get_default_wasapi_loopback()['name']\n"
            "mic_name = pa.get_default_input_device_info()['name']\n"
            "pa.terminate()\n"
            "print(json.dumps({'sys_name': sys_name, 'mic_name': mic_name}))\n"
        )

        result = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True
        )
        return json.loads(result.stdout)

    async def start(self) -> None:
        """
        Start the subprocess for the audio streamer and TCP server.
        """
        self.previous_device_names = await self._get_device_names()
        self.subprocess = await self._launch_subprocess()

    async def stop(self) -> None:
        """
        Stop the subprocess for the audio streamer and TCP server.
        """
        if self.subprocess and self.subprocess.returncode is None:
            await self.send_command("stop")
            try:
                await asyncio.wait_for(
                    self.subprocess.wait(), timeout=self.cfg.WAIT_DURATION_SECONDS
                )
            except TimeoutError:
                self.subprocess.terminate()
                try:
                    await asyncio.wait_for(
                        self.subprocess.wait(), timeout=self.cfg.WAIT_DURATION_SECONDS
                    )
                except TimeoutError:
                    self.subprocess.kill()
                    await self.subprocess.wait()

    async def device_check(self) -> None:
        """
        On-demand device check; restart subprocess if any changes are detected.
        """
        current_device_names = await self._get_device_names()
        if current_device_names != self.previous_device_names:
            await self.stop()
            self.subprocess = await self._launch_subprocess()
            self.previous_device_names = current_device_names

    async def send_command(self, cmd: str) -> str:
        """
        Send a one-off command to the audio streamer over the TCP connection.

        Args:
            cmd (str): Command to send to the audio streamer over the TCP connection.

        Returns:
            str: Response from the TCP server.
        """
        reader, writer = await asyncio.open_connection(
            self.cfg.AUDIO_STREAMER_TCP_HOST, self.cfg.AUDIO_STREAMER_TCP_PORT
        )
        writer.write(cmd.encode())
        await writer.drain()
        response = await reader.read(self.cfg.MAX_READ_BYTES)
        writer.close()
        await writer.wait_closed()
        return response.decode().strip()
