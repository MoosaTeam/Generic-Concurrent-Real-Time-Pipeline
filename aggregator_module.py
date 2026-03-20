class AggregatorModule:
    def __init__(self, config_dict, verified_queue, processed_queue):
        """
        Initializes the single Aggregator node.
        It collects authenticated data from the Core Workers and processes it sequentially.
        """
        self.verified_queue = verified_queue
        self.processed_queue = processed_queue

        # Extract the window size from the config object
        self.window_size = config_dict.window_size

    def _pure_running_average(self, new_value, current_window, max_size):
        """
        Purely functional transformation.
        Takes inputs and returns a NEW state and result without mutating variables.
        """
        updated_window = current_window + (new_value,)

        if len(updated_window) > max_size:
            updated_window = updated_window[1:]

        avg = sum(updated_window) / len(updated_window)
        return updated_window, avg

    def run_aggregator(self):
        """
        The continuous loop that acts as the 'Imperative Shell' around our functional core.
        """
        print("[Aggregator] Started sequencing and processing verified data...")

        # State is maintained locally within the process loop
        current_window = ()

        while True:
            # 1. Pull from the Verified Data Stream (blocks until data is available)
            packet = self.verified_queue.get()

            # Handle poison pill for graceful shutdown
            if packet is None:
                self.processed_queue.put(None)
                break

            metric = packet.get("metric_value")

            if metric is not None:
                # 2. Apply purely functional transformation
                current_window, avg = self._pure_running_average(
                    metric, current_window, self.window_size
                )

                # 3. Add the computed result to the packet
                packet["computed_metric"] = avg

                # 4. Push to the Final Processed Data Stream (Aggregator -> Output)
                self.processed_queue.put(packet)
