import asyncio
from asyncio import Event, StreamReader, StreamWriter

from voice.config.config import Config
from voice.models.audio_streamer.audio_streamer import AudioStreamer


async def _ipc_handler(
    reader: StreamReader,
    writer: StreamWriter,
    audio_streamer: AudioStreamer,
    stop_event: Event,
) -> None:
    """
    Handle incoming IPC commands to the TCP server.

    Args:
        reader (StreamReader): Stream reader for recieving data.
        writer (StreamWriter): Stream writer for sending responses.
        audio_streamer (AudioStreamer): Audio streamer to control.
        stop_event (Event): Signal to stop the server.
    """
    try:
        if not (data := await reader.read(audio_streamer.cfg.MAX_READ_BYTES)):
            writer.write(b"no data")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        cmd = data.decode().strip()

        match cmd:
            case "start_stream":
                audio_streamer.start_stream()
                writer.write(b"started")
            case "pause_stream":
                audio_streamer.pause_stream()
                writer.write(b"paused")
            case "stop":
                stop_event.set()
                writer.write(b"stopped")
            case _:
                writer.write(b"unkown command")

        await writer.drain()
        writer.close()
        await writer.wait_closed()

    except Exception:
        try:
            writer.write(b"error")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


async def main() -> None:
    """
    Run the TCP server for handling IPC with audio streamer.
    """
    stop_event = Event()

    cfg = Config()
    audio_streamer = AudioStreamer(cfg)

    await audio_streamer.start()

    server = await asyncio.start_server(
        lambda r, w: _ipc_handler(r, w, audio_streamer, stop_event),
        host=cfg.AUDIO_STREAMER_TPC_HOST,
        port=cfg.AUDIO_STREAMER_TPC_PORT,
    )

    async with server:
        await stop_event.wait()

    await audio_streamer.stop()

    await audio_streamer.stop()
