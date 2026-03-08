import csv
import time


class InputModule:
    def __init__(self, config, raw_queue):
        """
        Initializes the strictly decoupled Input module[cite: 9].
        It is completely unaware of the specific dataset domain.
        """
        self.config = config
        self.raw_queue = raw_queue
        self.dataset_path = self.config.dataset_path
        self.delay = self.config.input_delay_seconds
        self.schema = self.config.schema_columns

    def run(self):
        """
        Dynamically reads incoming files and streams them to the core workers.
        """
        print(f"[InputModule] Starting data ingestion from {self.dataset_path}...")

        try:
            with open(self.dataset_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)

                # 1. Read the raw header to dynamically find column indices
                try:
                    headers = next(reader)
                except StopIteration:
                    print("[InputModule] Dataset is empty.")
                    return

                # 2. Build a dynamic map of (CSV Column Index) -> (Internal Mapping & Type)
                # This ensures we only map what the config strictly defines.
                col_mapping = {}
                for col_def in self.schema:
                    source_name = col_def.get("source_name")
                    if source_name in headers:
                        idx = headers.index(source_name)
                        col_mapping[idx] = {
                            "internal": col_def.get("internal_mapping"),
                            "type": col_def.get("data_type"),
                        }
                    else:
                        print(
                            f"[InputModule] Warning: Configured column '{source_name}' not found in CSV headers."
                        )

                # 3. Stream the rows continuously [cite: 16]
                for row in reader:
                    generic_packet = {}

                    for idx, mapping in col_mapping.items():
                        # Extract the raw string value from the row
                        raw_value = row[idx].strip() if idx < len(row) else ""
                        internal_key = mapping["internal"]
                        expected_type = mapping["type"]

                        # 4. Cast the data to the correct primitive types
                        try:
                            if expected_type == "integer":
                                generic_packet[internal_key] = int(raw_value)
                            elif expected_type == "float":
                                generic_packet[internal_key] = float(raw_value)
                            else:  # default to string
                                generic_packet[internal_key] = str(raw_value)
                        except ValueError:
                            # If a specific cast fails (e.g., missing data), set to None
                            generic_packet[internal_key] = None

                    # 5. Push data packets into the bounded multiprocessing.Queue [cite: 16]
                    # Note: If input speed exceeds core processing capacity, the queue fills up.
                    # The .put() method inherently blocks when the queue is full,
                    # automatically creating the required backpressure.
                    self.raw_queue.put(generic_packet)

                    # 6. Throttle the input speed based on the config [cite: 18]
                    time.sleep(self.delay)

        except FileNotFoundError:
            print(
                f"[InputModule] Error: Could not find dataset at '{self.dataset_path}'."
            )
        except Exception as e:
            print(f"[InputModule] Unexpected error during ingestion: {e}")
        finally:
            print("[InputModule] Data stream finished or interrupted.")
