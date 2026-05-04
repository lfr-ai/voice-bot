"""Health-check endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Request

from ekko.core.enums import QueueName
from ekko.core.registry_constants import ROUTE_HEALTH
from ekko.presentation.api.schemas.responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get(ROUTE_HEALTH, response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    """Lightweight health check reporting TCP servers and queue status."""
    state = getattr(request.app, "state", None)
    ok = True
    details: dict = {}
    if state is None:
        return HealthResponse(ok=False, details={"reason": "app has no state"})

    details["sys_server_listening"] = bool(getattr(state, "sys_server", None))
    details["mic_server_listening"] = bool(getattr(state, "mic_server", None))
    qm = getattr(state, "queue_manager", None)
    if qm is None:
        details["queue_manager"] = "missing"
        ok = False
    else:
        try:
            details["transcripts_queue_present"] = QueueName.TRANSCRIPTS in qm.queues
        except Exception:
            details["transcripts_queue_present"] = False
            ok = False

    return HealthResponse(ok=ok, details=details)
