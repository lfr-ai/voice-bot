"""Audio stream control endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter(tags=["stream"])


@router.post("/start_stream")
async def start_stream(request: Request) -> dict:
    """Start audio streaming."""
    await request.app.state.controller.device_check()
    await request.app.state.controller.send_command("start_stream")
    return {"status": "started"}


@router.post("/pause_stream")
async def pause_stream(request: Request) -> dict:
    """Pause audio streaming."""
    await request.app.state.controller.send_command("pause_stream")
    return {"status": "paused"}
