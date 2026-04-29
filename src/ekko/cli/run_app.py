"""Small entrypoint script used for local runs and PyInstaller builds.

This keeps the executable entrypoint separate from the web framework
module and keeps the app import path stable.
"""

from __future__ import annotations

import os

import uvicorn


def main() -> None:
    host = os.getenv("EKKO_HOST", "127.0.0.1")
    port = int(os.getenv("EKKO_PORT", "8000"))
    reload = os.getenv("EKKO_RELOAD", "false").lower() == "true"
    uvicorn.run("ekko.composition.app_factory:create_app", factory=True, host=host, port=port, reload=reload)


if __name__ == "__main__":
    main()
