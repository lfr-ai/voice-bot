# Database (PostgreSQL) & migrations

This project uses SQLAlchemy (async) and Alembic for schema migrations.

Files of interest

- `src/voice/infrastructure/db/engine.py` — async engine and session factory
- `src/voice/infrastructure/db/models.py` — declarative Base and example models
- `alembic/` — Alembic environment and migration scripts

Quickstart (local dev)

```bash
# create venv and install deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# set DATABASE_URL/VOICE_POSTGRESQL_* via .env
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

This project uses SQLAlchemy 2.x async with `asyncpg` as the Postgres driver.

Location of DB helpers: `src/voice/infrastructure/db` (engine & session factory).

Quickstart

1. Install dependencies: `pdm install` or `pip install -r requirements.txt`.
2. Ensure Postgres is running locally and update `.env` / `DATABASE_URL`.
3. Run Alembic migrations:

```bash
alembic upgrade head
```

Notes

- Alembic is configured for async usage in `alembic/env.py` and imports the
  SQLAlchemy `Base` from `voice.infrastructure.db` so models are discovered
  when running `alembic revision --autogenerate`.
