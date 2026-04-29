"""Application entrypoint.

Delegates to the composition root for app creation.
Routes are defined in ``voice.presentation.api.routes``.
"""

import uvicorn

from voice.composition import create_app
from voice.config.settings import get_settings

app = create_app()


def main():
    settings = get_settings()
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
