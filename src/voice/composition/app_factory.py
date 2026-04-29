"""Application factory that wires the FastAPI app with routers and lifespan."""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
from queue import Empty

from fastapi import FastAPI

from voice.config.logging_config import configure_logging
from voice.config.settings import get_settings
from voice.infrastructure.adapters.audio_streamer_adapter import (
    create_audio_streamer_controller,
)
from voice.infrastructure.adapters.stt_adapter import create_faster_whisper_stt
from voice.managers.queue_manager import QueueManager
from voice.presentation.api.routes import health_router, stream_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Composition root lifespan. Uses adapter factories to satisfy core Protocols."""
    settings = get_settings()

    app.state.queue_manager = QueueManager()
    try:
        app.state.queue_manager.create_queue("transcripts")
    except Exception as e:
        logger.debug("Queue 'transcripts' already present or failed to create: %s", e)

    app.state.controller = create_audio_streamer_controller(settings)

    def _on_transcript(transcript):
        try:
            app.state.queue_manager.put_in_queue("transcripts", transcript)
        except Exception as e:
            logger.debug("Failed to put transcript into queue: %s", e)

    app.state.stt = create_faster_whisper_stt(
        settings=settings, model_name="small", batch_seconds=5, on_transcript=_on_transcript
    )

    await app.state.stt.ensure_queue("sys-queue")
    await app.state.stt.ensure_queue("mic-queue")
    await app.state.stt.start()

    host = settings.host
    sys_port = settings.audio_streamer_tcp_port + 1
    mic_port = settings.audio_streamer_tcp_port + 2

    async def _audio_receiver(reader, writer, queue_name: str):
        try:
            while True:
                data = await reader.read(settings.audio_frames_per_buffer * 2 * settings.audio_channels)
                if not data:
                    break
                await app.state.stt.accept_bytes(queue_name, data)
        except Exception as e:
            logger.debug("Audio receiver error for %s: %s", queue_name, e)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                logger.debug("Failed to close writer: %s", e)

    app.state.sys_server = await asyncio.start_server(lambda r, w: _audio_receiver(r, w, "sys-queue"), host, sys_port)
    app.state.mic_server = await asyncio.start_server(lambda r, w: _audio_receiver(r, w, "mic-queue"), host, mic_port)
    logger.info("Audio servers listening on %s:%s (sys) and %s:%s (mic)", host, sys_port, host, mic_port)

    await app.state.controller.start()

    app.state.async_transcript_queue = asyncio.Queue()

    async def _drain_transcripts_loop():
        qm = app.state.queue_manager
        q = qm.get_queue("transcripts")
        try:
            while True:
                try:
                    transcript = await asyncio.to_thread(q.get, True, 1)
                except Empty:
                    await asyncio.sleep(0.1)
                    continue
                try:
                    await app.state.async_transcript_queue.put(transcript)
                finally:
                    try:
                        q.task_done()
                    except Exception as e:
                        logger.debug("Failed to task_done on queue: %s", e)
        except asyncio.CancelledError:
            return

    app.state._transcript_bridge_task = asyncio.create_task(_drain_transcripts_loop())

    yield

    await app.state.controller.stop()
    await app.state.stt.stop()

    task = getattr(app.state, "_transcript_bridge_task", None)
    if task:
        task.cancel()
        try:
            await task
        except Exception as e:
            logger.debug("Transcript bridge task cancel/wait raised: %s", e)


def create_app() -> FastAPI:
    """Create and return a FastAPI application wired with routers."""
    app = FastAPI(lifespan=_lifespan)

    configure_logging()

    # Include presentation routers
    app.include_router(health_router)
    app.include_router(stream_router)

    # Attach LangChain adapter if available
    try:
        from voice.infrastructure.adapters.langchain_adapter import (
            LangChainOpenAIAdapter,
        )

        app.state.openai_adapter = LangChainOpenAIAdapter()
    except Exception as e:  # pragma: no cover
        logger.debug("LangChain adapter not available: %s", e)
        app.state.openai_adapter = None

    return app
