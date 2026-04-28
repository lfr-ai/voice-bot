FROM mcr.microsoft.com/devcontainers/python:1-3.11

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git curl ca-certificates zsh \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
RUN pip install uv pre-commit

WORKDIR /workspace

CMD ["/bin/bash"]
