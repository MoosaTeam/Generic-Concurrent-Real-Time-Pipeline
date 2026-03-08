================================================================================
Project Phase 3: Generic Concurrent Real-Time Pipeline
================================================================================

Creators:
- Muhammad Moosa: 24L-0561
- Syed Abdullah: 24L-0595

OVERVIEW:
---------
This system is a generalized, domain-agnostic, concurrent data-processing 
pipeline. It dynamically ingests, processes, and visualizes unseen datasets 
strictly based on a JSON configuration file. It utilizes Python's 
`multiprocessing` library to achieve parallel execution via a Producer-Consumer 
architecture, complete with real-time backpressure telemetry implemented via 
the Observer pattern.

DIRECTORY STRUCTURE & SETUP:
----------------------------
For the pipeline to execute correctly, the files must be organized as follows:

/ (Root Directory)
|-- main.py                 <-- THE MAIN EXECUTABLE
|-- config.json             <-- Configuration file
|-- config_parser.py
|-- input_module.py
|-- core_module.py
|-- output_module.py
|-- telemetry.py
|-- readme.txt
|-- diagrams/               <-- Contains PlantUML codes and generated images
|-- data/                   <-- PLACE THE UNSEEN DATASET HERE
    |-- unseen_dataset.csv

HOW TO RUN FOR FINAL EVALUATION (TA INSTRUCTIONS):
--------------------------------------------------
1. Extract the zip file contents.
2. Place your evaluation dataset inside the `data/` folder.
3. Replace or modify the `config.json` file in the root directory to match the 
   unseen dataset's schema and your desired pipeline dynamics.
4. Open a terminal at the root directory and execute:
   
   python main.py

IMPORTANT HARDWARE NOTE:
------------------------
The pipeline's concurrency is dictated by the `core_parallelism` value in 
`config.json`. If you run this on a machine with a lower core count (e.g., a 
dual-core processor), setting `core_parallelism` to 3 or higher will cause 
severe CPU bottlenecking and terminal tearing. Adjust `core_parallelism` in 
the configuration file according to the host machine's physical hardware 
capabilities.

ARCHITECTURE HIGHLIGHTS:
------------------------
- Strict Decoupling: The Input, Core, and Output modules are strictly locked 
  and domain-agnostic.
- The Functional Core: The Core workers process data streams using purely 
  functional logic, avoiding mutable global variables to prevent race conditions 
  in the multiprocessing queues.
- Telemetry & Observer Pattern: The dashboard UI strictly observes the queue 
  capacities independently, displaying visual indicators (Green/Yellow/Red) 
  as backpressure naturally builds when input speed exceeds core processing.
- Graceful Shutdown: The pipeline utilizes poison pills passed through the 
  multiprocessing queues to cleanly terminate all workers once the EOF is reached.

================================================================================
