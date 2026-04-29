from collections.abc import Callable
from threading import Event, Thread
from typing import Any


class ThreadManager:
    """Manager for threads.

    Tracks started threads and exposes a simple stop mechanism via an Event.
    """

    def __init__(self) -> None:
        """Initialize the ThreadManager."""
        self.threads: list[Thread] = []
        self.stop_event = Event()

    def start_thread(
        self,
        target: Callable[..., None],
        /,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Start a new daemon thread and track it.

        Args:
            target: Callable to run in the new thread.
            *args: Positional args for the target.
            **kwargs: Keyword args for the target.
        """
        thread = Thread(target=target, args=args, kwargs=kwargs, daemon=True)
        self.threads.append(thread)
        thread.start()

    def stop_all_threads(self) -> None:
        """Set the stop event to request shutdown and wait for threads to finish."""
        self.stop_event.set()
        self._wait_for_threads()

    def _wait_for_threads(self, timeout: float | None = None) -> None:
        """Wait for all living threads to finish.

        Args:
            timeout: Maximum wait time in seconds for each thread (or None to wait indefinitely).
        """
        for thread in self.threads:
            if thread and thread.is_alive():
                thread.join(timeout)
