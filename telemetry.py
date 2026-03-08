from abc import ABC, abstractmethod
import multiprocessing


# 1. The Observer Interface
class Observer(ABC):
    """
    Abstract interface for all observers.
    The OutputModule will implement this to receive queue size updates.
    """

    @abstractmethod
    def update(self, q1_size: int, q2_size: int):
        pass


# 2. The Subject
class PipelineTelemetry:
    def __init__(
        self, raw_queue: multiprocessing.Queue, processed_queue: multiprocessing.Queue
    ):
        """
        Initializes the telemetry monitor with references to the pipeline's queues.
        """
        self._observers = []
        self.raw_queue = raw_queue
        self.processed_queue = processed_queue

    def attach(self, observer: Observer):
        """
        Subscribes an observer to telemetry updates.
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print("[Telemetry] Observer attached successfully.")

    def notify(self, q1_size: int, q2_size: int):
        """
        Pushes the latest queue sizes to all subscribed observers.
        """
        for observer in self._observers:
            observer.update(q1_size, q2_size)

    def poll_queues(self):
        """
        Polls the current size of both queues and triggers a notification.
        This will be called continuously during the Output/Dashboard loop.
        """
        try:
            # .qsize() checks how full the queues are to monitor backpressure
            q1_size = self.raw_queue.qsize()
            q2_size = self.processed_queue.qsize()

            self.notify(q1_size, q2_size)

        except NotImplementedError:
            # Note: multiprocessing.Queue.qsize() raises NotImplementedError on macOS.
            # If you are on a Mac, you might need a different workaround or just pass -1.
            self.notify(-1, -1)
        except Exception as e:
            print(f"[Telemetry] Error polling queues: {e}")
