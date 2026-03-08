import multiprocessing
import time
from config_parser import PipelineConfig

# Imports for the modules we have built
from input_module import InputModule
from core_module import CoreModule
from output_module import OutputModule
from telemetry import PipelineTelemetry


def main():
    # 1. Load the configuration
    config = PipelineConfig()

    print("Initializing Generic Concurrent Real-Time Pipeline...")

    # 2. Create the bounded multiprocessing queues
    # This is what creates the natural backpressure. If the Core workers are too slow,
    # the raw_queue fills up, and the Input module is physically blocked from pushing more.
    raw_queue = multiprocessing.Queue(maxsize=config.stream_queue_max_size)
    processed_queue = multiprocessing.Queue(maxsize=config.stream_queue_max_size)

    # 3. Instantiate the isolated modules and Telemetry (Subject)
    telemetry = PipelineTelemetry(raw_queue, processed_queue)
    input_module = InputModule(config, raw_queue)
    core_module = CoreModule(config, raw_queue, processed_queue)
    output_module = OutputModule(config, processed_queue, telemetry)

    processes = []

    # 4. Wrap and Start the Input Process (Producer)
    p_input = multiprocessing.Process(target=input_module.run)
    processes.append(p_input)
    p_input.start()

    # 5. Wrap and Start the Core Worker Processes
    # We loop here to create multiple independent workers pulling from the same raw_queue
    for i in range(config.core_parallelism):
        p_core = multiprocessing.Process(target=core_module.run_worker)
        processes.append(p_core)
        p_core.start()

    # 6. Wrap and Start the Output/Dashboard Process (Consumer/Observer)
    p_output = multiprocessing.Process(target=output_module.render_dashboard)
    processes.append(p_output)
    p_output.start()

    print(f"Pipeline running with {config.core_parallelism} core workers.")
    print("Press Ctrl+C to terminate.")

    # 7. Graceful shutdown handler
    try:
        # In a real continuous stream, we'd wait for a poison pill.
        # For now, we block the main thread from exiting while workers run.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Terminating pipeline...")
        # Clean up all running child processes
        for p in processes:
            p.terminate()
            p.join()
        print("Pipeline shut down safely.")


if __name__ == "__main__":
    # You MUST use this if __name__ block when working with multiprocessing in Python,
    # otherwise you will spawn infinite recursive processes.
    main()
