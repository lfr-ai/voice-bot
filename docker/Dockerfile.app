FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install uv
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

COPY src/ ./src/

CMD ["sh","-lc","uv run uvicorn voice.interaction.main:app --host 0.0.0.0 --port 8000 || python -m uvicorn voice.interaction.main:app --host 0.0.0.0 --port 8000"]
