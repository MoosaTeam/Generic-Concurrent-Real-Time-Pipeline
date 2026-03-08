import csv
import time
from typing import Dict, Any
from core.contracts import StreamWriter


class GenericCSVProducer:
    """
    Phase 3 Input Module: A Domain-Agnostic Producer.
    Reads a CSV, maps/casts fields according to config, and pushes to a queue.
    """

    def run(self, out_stream: StreamWriter, config: Dict[str, Any]) -> None:
        # Extract configuration settings
        filepath = config.get("dataset_path", "")
        dynamics = config.get("pipeline_dynamics", {})
        delay = dynamics.get("input_delay_seconds", 0.0)

        # Extract the dynamic schema mapping
        schema = config.get("schema_mapping", {}).get("columns", [])

        if not filepath or not schema:
            print("❌ Producer Error: Missing filepath or schema in config.")
            return

        print(f"📥 Producer Starting: Ingesting {filepath}...")

        try:
            with open(filepath, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # 1. Create a generic data packet based strictly on the schema
                    packet = {}
                    for col_def in schema:
                        src_name = col_def["source_name"]
                        internal_name = col_def["internal_mapping"]
                        target_type = col_def["data_type"]

                        raw_value = row.get(src_name, "")

                        # 2. Cast to the correct primitive type
                        packet[internal_name] = self._cast_value(raw_value, target_type)

                    # 3. Push to the Raw Data Stream
                    # If the Core workers are too slow, the queue fills up and this .put()
                    # blocks, naturally creating backpressure throttling.
                    out_stream.put(packet)

                    # 4. Simulate stream delay (Throttling)
                    if delay > 0:
                        time.sleep(delay)

        except FileNotFoundError:
            print(f"❌ Producer Error: File {filepath} not found.")
            return

        # 5. Send 'Poison Pills' (EOF markers) to tell the Core workers to stop.
        # We must send one for each concurrent core worker running.
        parallelism = dynamics.get("core_parallelism", 1)
        for _ in range(parallelism):
            out_stream.put({"EOF": True})

        print("📥 Producer Finished: All data pushed to Raw Stream.")

    def _cast_value(self, value: str, data_type: str) -> Any:
        """Dynamically casts the raw string to the required primitive type."""
        if not value or value.lower() == "nan":
            if data_type == "integer":
                return 0
            if data_type == "float":
                return 0.0
            return ""

        try:
            if data_type == "integer":
                return int(float(value))  # float() first in case string is "2020.0"
            elif data_type == "float":
                return float(value)
            else:  # Default to string
                return str(value)
        except ValueError:
            # Fallbacks for corrupted data
            if data_type == "integer":
                return 0
            if data_type == "float":
                return 0.0
            return str(value)
