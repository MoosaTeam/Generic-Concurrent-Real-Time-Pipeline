from typing import Protocol, Any, Dict


class StreamWriter(Protocol):
    """Abstraction for putting data into a queue/stream."""

    def put(
        self, item: Any, block: bool = True, timeout: float | None = None
    ) -> None: ...


class StreamReader(Protocol):
    """Abstraction for pulling data out of a queue/stream."""

    def get(self, block: bool = True, timeout: float | None = None) -> Any: ...


class DataProducer(Protocol):
    """
    Input Module Contract: Reads a file and pushes generic data packets
    into the Raw Data Stream.
    """

    def run(self, out_stream: StreamWriter, config: Dict[str, Any]) -> None: ...


class DataTransformer(Protocol):
    """
    Core Module Contract: Pulls from Raw Stream, processes functionally,
    and pushes to Processed Data Stream.
    """

    def run(
        self, in_stream: StreamReader, out_stream: StreamWriter, config: Dict[str, Any]
    ) -> None: ...


class DataConsumer(Protocol):
    """
    Output Module Contract: Pulls from Processed Data Stream and
    updates real-time visualizations.
    """

    def run(self, in_stream: StreamReader, config: Dict[str, Any]) -> None: ...
