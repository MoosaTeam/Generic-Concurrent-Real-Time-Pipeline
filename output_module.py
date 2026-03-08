import os
import time
from telemetry import Observer, PipelineTelemetry

class OutputModule(Observer):
    def __init__(self, config, processed_queue, telemetry: PipelineTelemetry):
        """
        Initializes the Dashboard. It is an Observer that renders real-time data.
        """
        self.config = config
        self.processed_queue = processed_queue
        self.telemetry = telemetry
        
        # Subscribe this module to the telemetry subject 
        self.telemetry.attach(self)
        
        self.max_q_size = self.config.stream_queue_max_size
        self.q1_size = 0
        self.q2_size = 0

        # Extract dynamic chart configurations
        self.charts = self.config.visualizations.get("data_charts", [])
        self.telemetry_config = self.config.visualizations.get("telemetry", {})
        
        # Simple buffer for rendering the "charts" in the console
        self.history = []

    def update(self, q1_size: int, q2_size: int):
        """
        Triggered by the Telemetry Subject to update queue capacities.
        """
        self.q1_size = q1_size
        self.q2_size = q2_size

    def _get_color_indicator(self, current_size):
        """
        Evaluates backpressure and returns color-coded warnings.
        Green = flowing smoothly, Yellow = queue filling, Red = heavy backpressure[cite: 29].
        """
        ratio = current_size / self.max_q_size if self.max_q_size > 0 else 0
        if ratio >= 0.8:
            return "\033[91m[RED - Heavy Backpressure]\033[0m"
        elif ratio >= 0.5:
            return "\033[93m[YELLOW - Filling]\033[0m"
        else:
            return "\033[92m[GREEN - Smooth]\033[0m"

    def _render_telemetry(self):
        """Renders the health of the two independent streams."""
        print("=== PIPELINE TELEMETRY ===")
        if self.telemetry_config.get("show_raw_stream", True):
            print(f"Raw Stream (Input -> Core):       {self.q1_size:02d}/{self.max_q_size} " 
                  f"{self._get_color_indicator(self.q1_size)}")
        if self.telemetry_config.get("show_processed_stream", True):
            print(f"Processed Stream (Core -> Output): {self.q2_size:02d}/{self.max_q_size} "
                  f"{self._get_color_indicator(self.q2_size)}")
        print("==========================\n")

    def render_dashboard(self):
        """
        Main loop for the Output process. Pulls data and redraws the UI.
        """
        while True:
            # 1. Ask the telemetry monitor to poll queues and notify us
            self.telemetry.poll_queues()

            # 2. Pull from Processed Data Stream (Core -> Output)
            try:
                # Timeout prevents the UI from freezing if the core workers are slow
                packet = self.processed_queue.get(timeout=0.1)
                
                # Check for a poison pill to shut down gracefully
                if packet is None:
                    break
                
                self.history.append(packet)
                if len(self.history) > 10:
                    self.history.pop(0)
                    
            except Exception:
                # Queue is empty, just pass and redraw the UI with current state
                pass

            # 3. Clear terminal for a real-time dashboard feel
            os.system('cls' if os.name == 'nt' else 'clear')

            # 4. Render Telemetry Backpressure Indicators
            self._render_telemetry()
            
            # 5. Render Dynamic Charts
            print("=== LIVE DATA FEED ===")
            for chart in self.charts:
                title = chart.get("title")
                y_axis = chart.get("y_axis")
                x_axis = chart.get("x_axis")
                print(f"[{title}]")
                
                # Show the last 5 data points
                for pt in self.history[-5:]:
                    x_val = pt.get(x_axis, "N/A")
                    if y_axis in pt:
                        y_val = f"{pt[y_axis]:.2f}" if isinstance(pt[y_axis], float) else pt[y_axis]
                        print(f"  {x_val}: {y_val}")
                print()
            
            # Throttle the UI loop so it doesn't flicker violently
            time.sleep(0.1)
