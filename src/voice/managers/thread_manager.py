from threading import Event, Thread
from typing import Any, Callable


class ThreadManager:
    """
    Manager for threads.
    """

    def __init__(self):
        """
        Initialize the ThreadManager.
        """
        self.threads = []
        self.stop_event = Event()

    def start_thread(
        self, target: Callable[..., None], args: tuple = (), kwargs: dict[str, Any] = {}
    ) -> None:
        """
        Start a new thread and track it.

        Args:
            target (callable): Target function to run in the thread.
            args (tuple): Positional argument values to pass to the target function.
            kwargs (dict): Keyword argument values to pass to the target function.
        """
        thread = Thread(target=target, args=args, kwargs=kwargs)
        self.threads.append(thread)
        thread.start

    def stop_all_threads(self) -> None:
        """
        Set the stop event to stop all threads.
        """
        self.stop_event.set()
        self._wait_for_threads()

    def _wait_for_threads(self, timeout: float | int | None = None) -> None:
        """
        Wait for all lviing threads to finish.

        Args:
            timeout (float | int | None): Maximum wait time in seconds.
        """
        for thread in self.threads:
            if thread and thread.is_alive():
                thread.join(timeout)
