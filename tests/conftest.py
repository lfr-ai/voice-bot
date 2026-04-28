"""Pytest configuration and test bootstrap helpers."""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    """Ensure local source directory is importable in test sessions."""

    src_path = Path(__file__).resolve().parents[1] / "src"
    src_str = str(src_path)
    if src_str not in sys.path:
        sys.path.insert(0, src_str)


_ensure_src_on_path()
