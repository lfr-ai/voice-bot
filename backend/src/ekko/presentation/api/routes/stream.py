"""Audio stream control endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Request

from ekko.presentation.api.schemas.responses import StreamResponse

router = APIRouter(tags=["stream"])


@router.post("/start_stream", response_model=StreamResponse)
async def start_stream(request: Request) -> StreamResponse:
    """Start audio streaming."""
    await request.app.state.controller.device_check()
    await request.app.state.controller.send_command("start_stream")
    return StreamResponse(status="started")


@router.post("/pause_stream", response_model=StreamResponse)
async def pause_stream(request: Request) -> StreamResponse:
    """Pause audio streaming."""
    await request.app.state.controller.send_command("pause_stream")
    return StreamResponse(status="paused")
