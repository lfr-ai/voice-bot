from queue import Queue
from typing import Any


class QueueManager:
    """
    Manager for thread-safe FIFO queues.
    """

    def __init__(self):
        """
        Initialize the QueueManager.
        """
        self.queues: dict[str, Queue] = {}

    def create_queue(self, name: str) -> None:
        """
        Create a new queue with the specified name.

        Args:
            name (str): Name of the queue.
        """
        if not isinstance(name, str):
            raise TypeError("Queue name must be a string.")
        if name in self.queues:
            raise ValueError(f"Queue '{name}' already exists.")
        self.queues[name] = Queue()

    def get_queue(self, name: str) -> Queue:
        """
        Get the queue associated with the specified name.

        Args:
            name (str): Name of the queue.

        Returns:
            Queue: Requested queue.
        """
        try:
            return self.queues[name]
        except KeyError:
            raise KeyError(f"Queue '{name}' does not exist.")

    def put_in_queue(self, name: str, item: Any) -> None:
        """
        Put an item into the specified queue.

        Args:
            name (str): Name of the queue.
            item (Any): Item to put in the queue.
        """
        queue = self.get_queue(name)
        queue.put(item)

    def get_from_queue(self, name: str, timeout: float | int | None = None) -> Any:
        """
        Get an item from the specified queue.

        Args:
            name (str): Name of the queue.
            timeout (float | int | None): Maximum wait time in seconds.

        Returns:
            Any: Item from the queue.
        """
        queue = self.get_queue(name)
        return queue.get(timeout=timeout)

    def task_done(self, name: str) -> None:
        """
        Signal that a task from the specified queue is complete.

        Args:
            name (str): Name of the queue.
        """
        queue = self.get_queue(name)
        queue.task_done()

    def join_queue(self, name: str) -> None:
        """
        Block the specified queue until all items have been processed.

        Args:
            name (str): Name of the queue.
        """
        queue = self.get_queue(name)
        queue.join()

    def remove_queue(self, name: str) -> None:
        if name in self.queues:
            del self.queues[name]
        else:
            raise KeyError(f"Queue '{name}' does not exist.")
