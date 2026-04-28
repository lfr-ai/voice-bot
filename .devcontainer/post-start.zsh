#!/usr/bin/env zsh
set -eu

cd /workspace

if [ ! -d ".venv" ]; then
  uv sync --all-extras || true
fi
