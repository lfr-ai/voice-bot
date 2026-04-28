FROM python:3.13-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml .
COPY src ./src
RUN python -m venv .venv && . .venv/bin/activate && pip install --upgrade pip && pip install -e . || true
CMD ["/bin/bash"]
