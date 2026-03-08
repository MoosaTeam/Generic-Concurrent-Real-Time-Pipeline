<div align="center">

# 🚀 Generic Concurrent Real-Time Pipeline
*(aka: The Magic Data Tube That Somehow Works)*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Multiprocessing](https://img.shields.io/badge/Concurrency-Multiprocessing-success.svg)]()
[![Status](https://img.shields.io/badge/Status-It_Works!-brightgreen.svg)]()

**Survivors / Creators:**
Muhammad Moosa (24L-0561) • Syed Abdullah (24L-0595)

</div>

---

## 📌 What is this?

Look, we’re going to be honest: we built a concurrent, domain-agnostic data pipeline using Python’s `multiprocessing` library, and the fact that it hasn't spawned an infinite loop of terminal windows that crashes our laptops is a minor miracle. 

**Officially:** This system takes a basic data analysis script and elevates it into a generalized pipeline. It dynamically ingests, processes, and visualizes completely unseen datasets driven entirely by a `config.json` file. It uses true multi-core processing to simulate high-throughput data streams, complete with a real-time flashing dashboard. 

**Unofficially:** We built a machine that eats CSV files blindly, throws the data at multiple CPU cores to do math, and yells at us in Red, Yellow, or Green depending on how stressed out the system is.

## 🌊 How the Flow Actually Works 



We implemented a **Producer-Consumer architecture** bounded by multiprocessing queues. Here is the life cycle of our data:

1. **The Setup:** `main.py` reads the config, sets up two bounded queues (our data pipes), and spawns a bunch of independent parallel processes.
2. **The Ingestion:** The Input Module aggressively reads a CSV file line-by-line and shoves generic "data packets" into *Queue 1 (Raw Data)*. If Queue 1 gets full because the core workers are too slow, the Input Module gets physically blocked from pushing more. This is our **Natural Backpressure**.
3. **The Sweatshop:** Multiple Core Workers pull data from *Queue 1* simultaneously, do some purely functional math (strictly no mutable global variables here, just raw tuples!), and shove the result into *Queue 2 (Processed Data)*.
4. **The Snitch (Telemetry):** The Telemetry object (Subject) constantly spies on the sizes of both queues and reports back to the Dashboard (Observer). 
5. **The Pretty Colors:** The Output Module pulls the final data from *Queue 2*, furiously clears the terminal, and draws a live dashboard with Green/Yellow/Red health indicators based on what the Telemetry object told it.

## 🧩 The Modules (Who Does What)

| Module | Role | Description |
| :--- | :--- | :--- |
| `main.py` | **The Boss** | Wires the queues together, starts the parallel processes, and handles the `Ctrl+C` graceful shutdown so we don't leave zombie processes eating our RAM. |
| `config.json` | **The Brain** | The pipeline is completely oblivious to what "Climate" or "Temperature" is. It only knows what the JSON tells it to know. |
| `input_module.py` | **The Border Guard** | Maps raw, messy CSV headers to clean, internal generic variables and casts them to integers/floats so the rest of the pipeline doesn't crash. (Producer) |
| `core_module.py` | **The Heavy Lifter** | Calculates the running averages using strictly functional programming. Don't ask us how the immutable tuples work under the hood, just know they prevent race conditions. (Consumer/Producer) |
| `output_module.py`| **The UI** | Renders the data and gives us a live, flickering terminal dashboard. (Observer/Consumer) |
| `telemetry.py` | **The Snitch** | Implements the Observer Design Pattern to monitor queue capacities without tightly coupling the dashboard to the data streams. (Subject) |

## 📂 Directory Structure

For the pipeline to execute correctly, please keep our files exactly like this:

```text
/
├── main.py                 # Run this file to start the magic!
├── config.json             # The remote control. Change this to break things.
├── config_parser.py        # Translates the JSON so Python stops complaining.
├── input_module.py         # The hungry CSV reader.
├── core_module.py          # The functional math nerds.
├── output_module.py        # The shiny dashboard renderer.
├── telemetry.py            # The queue size snitch.
├── README.md               # You are reading this right now.
├── diagrams/               # Proof that we planned this before coding it.
└── data/                   # ⚠️ MR. TA: PLACE THE UNSEEN DATASET IN HERE! ⚠️
    └── unseen_dataset.csv  
🚀 Grading Instructions (How to Run)
[!IMPORTANT]

To the TA evaluating this: Please follow these steps to test our pipeline with your secret dataset.

Open config.json and change "dataset_path" to point to your secret test dataset inside the data/ folder.

Update the "schema_mapping" array in the JSON to match your secret dataset's columns.

Open your terminal in the root directory and run:

Bash
python main.py
Sit back and watch the multi-core backpressure do its thing!

[!TIP]
Want to test the Backpressure? Set "core_parallelism": 1 and "input_delay_seconds": 0.001 in the config if you want to see the terminal yell at you in RED. Then set "core_parallelism": 10 to watch the workers clear the bottleneck and return to GREEN.
