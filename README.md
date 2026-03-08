# Project Phase 3: Generic Concurrent Real-Time Pipeline

**Creators:**
- Muhammad Moosa (24L-0561)
- Syed Abdullah (24L-0595)

## 📌 Overview
[cite_start]This system elevates a basic data analysis script into a generalized, concurrent data-processing pipeline[cite: 3, 4]. [cite_start]It dynamically ingests, processes, and visualizes completely unseen datasets driven entirely by a JSON configuration file[cite: 5, 6]. 

[cite_start]By utilizing Python's standard `multiprocessing` library, the pipeline achieves true parallel execution via a Producer-Consumer architecture, complete with real-time dashboard telemetry that demonstrates system backpressure[cite: 7, 14].

## 🏗️ System Architecture & Constraints

* [cite_start]**Strict Decoupling:** The Input, Core, and Output modules are strictly locked and domain-agnostic[cite: 9, 10].
* [cite_start]**Producer-Consumer Streams:** Utilizes two bounded `multiprocessing.Queue` instances to pass generic data packets between isolated processes[cite: 16, 17]. 
* **The Functional Core:** The internal transformation logic of the Core workers (e.g., calculating a running average) is completely functional. [cite_start]We strictly avoid mutable global variables and standard append-based lists to prevent race conditions[cite: 20, 21, 22].
* [cite_start]**Telemetry via Observer Pattern:** The dashboard UI (Observer) subscribes to a Pipeline Telemetry object (Subject) to dynamically render real-time visual indicators of queue capacities (Green, Yellow, Red)[cite: 27, 29, 30, 32].
* [cite_start]**Natural Backpressure:** If the input stream exceeds the processing capacity of the core workers, the bounded queues naturally fill up, automatically throttling the Input module[cite: 19].

## 📂 Directory Structure

For the pipeline to execute correctly, the files must be organized as follows:

```text
/
├── main.py                 # The central orchestrator & main executable
├── config.json             # Configuration file dictating pipeline behavior
├── config_parser.py        # Logic for parsing the configuration file
├── input_module.py         # Dynamic ingestion & schema mapping (Producer)
├── core_module.py          # Functional processing workers (Consumers/Producers)
├── output_module.py        # Real-time dashboard UI (Observer/Consumer)
├── telemetry.py            # Queue monitoring (Subject)
├── README.md               # Project documentation
├── diagrams/               # Contains PlantUML codes and generated design artifacts
└── data/                   # PLACE THE UNSEEN DATASET HERE
    └── unseen_dataset.csv
