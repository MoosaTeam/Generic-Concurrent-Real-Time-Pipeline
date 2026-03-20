import json
import os


class PipelineConfig:
    def __init__(self, config_path="config.json"):
        """Loads and parses the configuration file."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at {config_path}")

        # THIS MUST HAPPEN FIRST! Load the JSON into self._config
        with open(config_path, "r") as file:
            self._config = json.load(file)

    # --- General ---
    @property
    def dataset_path(self):
        return self._config.get("dataset_path")

    @property
    def secret_key(self):
        return self._config.get("secret_key", "")

    # --- Pipeline Dynamics ---
    @property
    def input_delay_seconds(self):
        return self._config.get("pipeline_dynamics", {}).get(
            "input_delay_seconds", 0.01
        )

    @property
    def core_parallelism(self):
        return self._config.get("pipeline_dynamics", {}).get("core_parallelism", 1)

    @property
    def stream_queue_max_size(self):
        return self._config.get("pipeline_dynamics", {}).get(
            "stream_queue_max_size", 50
        )

    @property
    def window_size(self):
        return self._config.get("pipeline_dynamics", {}).get("window_size", 5)

    # --- Schema Mapping ---
    @property
    def schema_columns(self):
        """Returns the list of column mappings to cast types correctly."""
        return self._config.get("schema_columns", [])

    # --- Visualizations ---
    @property
    def visualizations(self):
        return self._config.get("visualizations", {})


if __name__ == "__main__":
    # Quick test to ensure it works
    config = PipelineConfig()
    print(f"Dataset Path: {config.dataset_path}")
    print(f"Secret Key: {config.secret_key}")
    print(f"Core Parallelism: {config.core_parallelism}")
    print(f"Columns to map: {len(config.schema_columns)}")
