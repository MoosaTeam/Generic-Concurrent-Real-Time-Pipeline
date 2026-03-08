class CoreModule:
    def __init__(self, config, raw_queue, processed_queue):
        """
        Initializes the Core Module, completely unaware of what the data represents[cite: 12].
        """
        self.config = config
        self.raw_queue = raw_queue
        self.processed_queue = processed_queue
        self.window_size = self.config.window_size

    def _pure_running_average(self, new_value, current_window, max_size):
        """
        Purely functional transformation.
        Takes inputs and returns a NEW state and result without mutating variables.
        """
        # Create a new tuple with the new value (tuples are immutable in Python)
        updated_window = current_window + (new_value,)
        
        # If we exceed the window size, slice to create a new tuple
        if len(updated_window) > max_size:
            updated_window = updated_window[1:]

        avg = sum(updated_window) / len(updated_window)
        return updated_window, avg

    def run_worker(self):
        """
        Pulls from the Raw Data Stream, performs operations, and pushes to Processed Stream[cite: 17].
        """
        print("[CoreWorker] Started processing stream...")
        
        # State is maintained locally within the process loop, NOT as a class attribute
        current_window = ()

        while True:
            # 1. Pull from Raw Data Stream (blocks until data is available) [cite: 17]
            packet = self.raw_queue.get()

            # Handle a poison pill for graceful shutdown (optional but good practice)
            if packet is None:
                break

            # The generic internal mapping we defined in the config
            metric = packet.get("metric_value")

            if metric is not None:
                # 2. Apply purely functional transformation 
                # We overwrite the local variable with the NEW state returned by the pure function
                current_window, computed_avg = self._pure_running_average(
                    metric, current_window, self.window_size
                )

                # Add the computed metric to the generic packet
                packet["computed_metric"] = computed_avg

            # 3. Push the results into the second bounded queue [cite: 17]
            self.processed_queue.put(packet)
