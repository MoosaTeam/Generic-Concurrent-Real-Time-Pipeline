import multiprocessing
import time
from config_parser import PipelineConfig

# Imports for all modules
from input_module import InputModule
from core_module import CoreModule
from aggregator_module import AggregatorModule
from output_module import OutputModule
from telemetry import PipelineTelemetry


def main():
    config = PipelineConfig()
    print("Initializing Secure Scatter-Gather Real-Time Pipeline...")

    # 1. Create THREE bounded multiprocessing queues
    max_q_size = config.stream_queue_max_size

    raw_queue = multiprocessing.Queue(maxsize=max_q_size)  # Input -> Core
    verified_queue = multiprocessing.Queue(maxsize=max_q_size)  # Core -> Aggregator
    processed_queue = multiprocessing.Queue(maxsize=max_q_size)  # Aggregator -> Output

    # 2. Setup Telemetry (Monitoring Raw and Processed queues)
    telemetry = PipelineTelemetry(raw_queue, processed_queue)

    # 3. Instantiate the Modules
    # CHANGED: Passing 'config' directly instead of 'config._config'
    input_module = InputModule(config, raw_queue)
    aggregator_module = AggregatorModule(config, verified_queue, processed_queue)
    output_module = OutputModule(config, processed_queue, telemetry)

    processes = []

    # 4. Start the Input Process (Producer)
    p_input = multiprocessing.Process(target=input_module.run)
    processes.append(p_input)
    p_input.start()

    # 5. Start the Parallel Core Workers (The Cryptographic Scatters)
    for i in range(config.core_parallelism):
        # CHANGED: Passing 'config' directly instead of 'config._config'
        core_module = CoreModule(config, raw_queue, verified_queue)
        p_core = multiprocessing.Process(target=core_module.run_worker)
        processes.append(p_core)
        p_core.start()

    # 6. Start the Single Aggregator Process (The Sequential Gatherer)
    p_aggregator = multiprocessing.Process(target=aggregator_module.run_aggregator)
    processes.append(p_aggregator)
    p_aggregator.start()

    # 7. Start the Output/Dashboard Process (Consumer/Observer)
    p_output = multiprocessing.Process(target=output_module.render_dashboard)
    processes.append(p_output)
    p_output.start()

    print(
        f"Pipeline running with {config.core_parallelism} security bouncers and 1 aggregator."
    )
    print("Press Ctrl+C to terminate.")

    # 8. Graceful shutdown handler
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Terminating pipeline...")
        for p in processes:
            p.terminate()
            p.join()
        print("Pipeline shut down safely.")


if __name__ == "__main__":
    main()
