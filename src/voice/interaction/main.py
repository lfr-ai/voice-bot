import uvicorn

from voice.composition import create_app
from voice.config.config import Config
from voice.utils.logger import Logger

cfg = Config()
logger = Logger.create(__name__, cfg.LOGS_DIR_PATH / "Backend.log")

# Use canonical composition root
app = create_app()


@app.post("/start_stream")
async def start_stream():
    """Start audio streaming."""
    await app.state.controller.device_check()
    await app.state.controller.send_command("start_stream")


@app.post("/pause_stream")
async def pause_stream():
    """Pause audio streaming."""
    await app.state.controller.send_command("pause_stream")


@app.get("/health")
async def health():
    """Lightweight health check reporting TCP servers and queue status."""
    state = getattr(app, "state", None)
    ok = True
    details: dict = {}
    if state is None:
        return {"ok": False, "reason": "app has no state"}

    details["sys_server_listening"] = bool(getattr(state, "sys_server", None))
    details["mic_server_listening"] = bool(getattr(state, "mic_server", None))
    qm = getattr(state, "queue_manager", None)
    if qm is None:
        details["queue_manager"] = "missing"
        ok = False
    else:
        try:
            details["transcripts_queue_present"] = "transcripts" in qm.queues
        except Exception:
            details["transcripts_queue_present"] = False
            ok = False

    return {"ok": ok, "details": details}


def main():
    uvicorn.run(app, host=cfg.HOST, port=cfg.PORT)


if __name__ == "__main__":
    main()
