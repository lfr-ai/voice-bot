from __future__ import annotations

from typing import Any, Protocol


class Transcript(Protocol):
    stream_name: str
    text: str
    segments: Any
    info: Any


class STTService(Protocol):
    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...

    async def ensure_queue(self, queue_name: str) -> None:
        ...

    async def accept_bytes(self, queue_name: str, data: bytes) -> None:
        ...


class AudioStreamerControllerProtocol(Protocol):
    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...

    async def device_check(self) -> None:
        ...

    async def send_command(self, cmd: str) -> str:
        ...
