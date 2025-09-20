from contextlib import asynccontextmanager
from typing import AsyncGenerator

import fastapi
import uvicorn
from fastapi import FastAPI, Path, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from voice.config.config import Config
from voice.managers.queue_manager import QueueManager
from voice.models.audio_streamer.audio_streamer_controller import (
    AudioStreamerController,
)
from voice.utils.logger import Logger

cfg = Config()

logger = Logger.create(__name__, cfg.LOGS_DIR_PATH / "Backend.log")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler for the backend.

    Args:
        app (FastAPI): FastAPI application.
    """
    app.state.queue_manager = QueueManager
    controller = AudioStreamerController(cfg)
    app.state.controller = controller
    await controller.start()
    yield
    await controller.stop()


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/start_stream")
async def start_stream():
    """
    Start sending audio to the WebSocket server.
    """
    controller = app.state.controller
    await controller.device_check()
    response = await controller.send_command("start_stream")


@app.post("/pause_stream")
async def pause_stream():
    """
    Pause sending audio to the WebSocket server.
    """
    response = await app.state.controller.send_command("pause_stream")


# @app.websocket("/ws/{stream_type}")
# async def websocket_stt(
#     websocket: WebSocket, stream_type: str = Path(..., description="Type of stream")
# ) -> None:
#     """ "
#     WebSocket for recieving audio for speech-to-text conversion.

#     Args:sss
#         websocket (WebSocket): WebSocket connection.
#         stream_type (str): Type of stream.
#     """♣
#     await websocket.accept()

#     queue_name = f"{stream_type}-queue"
#     queue_manager = app.state.queue_manager
#     # mode = RecognitionMode.from_stream_type(stream_type)

#     #stt = Transcriber(cfg, queue_name, queue_manager, mode)

#     stt.start()
#     try:
#         while True:
#             data = await websocket.receive_bytes()
#             stt.


def main() -> None:
    """
    Run the backend.
    """
    uvicorn.run(app, host=cfg.BACKEND_HOST, port=cfg.BACKEND_PORT)
