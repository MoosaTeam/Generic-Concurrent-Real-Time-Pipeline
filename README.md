<div align="center">

# 🚀 Generic Concurrent Real-Time Pipeline
*(aka: The Magic Data Tube That Somehow Works: Secure Edition)*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Concurrency](https://img.shields.io/badge/Concurrency-Scatter_Gather-success.svg)]()
[![Security](https://img.shields.io/badge/Security-PBKDF2_SHA256-critical.svg)]()
[![Status](https://img.shields.io/badge/Status-It_Works!-brightgreen.svg)]()

**Survivors / Creators:**
Muhammad Moosa (24L-0561) • Syed Abdullah (24L-0595)

</div>

---

## 📌 What is this?

Look, we’re going to be honest: we took our already complicated concurrent pipeline and injected military-grade cryptographic hashing into it. We implemented a full **Scatter-Gather** architecture using Python’s `multiprocessing` library, and the fact that it hasn't melted our CPUs into slag is a minor miracle. 

**Officially:** This system is a generalized, highly secure data pipeline. It dynamically ingests completely unseen datasets driven by a `config.json` file. It scatters raw data across multiple CPU cores to authenticate rows using a heavy PBKDF2 HMAC SHA-256 hash. Valid data is then gathered by a single aggregator to compute purely functional running averages before being sent to a real-time dashboard.

**Unofficially:** We built a machine that eats CSV files blindly, forces multiple CPU cores to act as cryptographic bouncers (who instantly drop fake data), funnels the survivors to a single math nerd, and yells at us in Red, Yellow, or Green depending on how stressed out the system is.

## 🌊 How the Flow Actually Works (Scatter-Gather)

We implemented a strict **Scatter-Gather architecture** bounded by three multiprocessing queues. Here is the life cycle of our data:

1. **The Setup:** `main.py` reads the config, sets up *three* bounded queues (our data pipes), and spawns our independent parallel processes.
2. **The Ingestion:** The Input Module aggressively reads a CSV file line-by-line and shoves generic "data packets" into *Queue 1 (Raw Data)*. This is where our **Natural Backpressure** begins.
3. **The Bouncers (Scatter Phase):** Multiple Core Workers pull data from *Queue 1* simultaneously. They don't do math anymore; they extract the raw value, combine it with our `secret_key`, and compute a massive 100,000-iteration hash. If the signature matches the CSV, the packet is pushed to *Queue 2 (Verified Data)*. If it's a fake, it gets silently dropped into the void.
4. **The Gatherer (Gather Phase):** Because the bouncers finish at different times, a single Aggregator process pulls from *Queue 2* to sequence the valid packets. It applies purely functional math to calculate running averages and pushes the results to *Queue 3 (Processed Data)*.
5. **The Snitch (Telemetry):** The Telemetry object (Subject) constantly spies on the sizes of the Raw and Processed queues and reports back to the Dashboard (Observer). 
6. **The Pretty Colors:** The Output Module pulls the final data from *Queue 3*, furiously clears the terminal, and draws a live dashboard with Green/Yellow/Red health indicators based on what the Telemetry object told it.

## 🧩 The Modules (Who Does What)

| Module | Role | Description |
| :--- | :--- | :--- |
| `main.py` | **The Boss** | Wires the 3 queues together, starts the parallel processes, and handles the `Ctrl+C` graceful shutdown so we don't leave zombie processes eating our RAM. |
| `config.json` | **The Brain** | The pipeline is completely oblivious to what "Climate" or "Temperature" is. It only knows what the JSON tells it to know. |
| `input_module.py` | **The Border Guard** | Maps raw, messy CSV headers to clean, internal generic variables. (Producer) |
| `core_module.py` | **The Security Bouncers** | Pulls raw data, computes heavy PBKDF2 hashes, verifies signatures, and drops unauthenticated rows. (Consumer/Producer) |
| `aggregator_module.py`| **The Math Nerd** | A single process that sequences verified data, maintains local state, and calculates running averages functionally. (Consumer/Producer) |
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
├── core_module.py          # The cryptographic bouncers (Scatter).
├── aggregator_module.py    # The running average calculator (Gather).
├── output_module.py        # The shiny dashboard renderer.
├── telemetry.py            # The queue size snitch.
├── README.md               # You are reading this right now.
├── diagrams/               # Proof that we planned this before coding it.
└── data/                   # ⚠️ MR. TA: PLACE THE UNSEEN DATASET IN HERE! ⚠️
    └── sample_sensor_data.csv  
🚀 Grading Instructions (How to Run)
[!IMPORTANT]

To the TA evaluating this: Please follow these steps to test our pipeline with your secret dataset.

Open config.json and change "dataset_path" to point to your secret test dataset inside the data/ folder.

Ensure you have updated the "secret_key" in the config if your new dataset uses a different key for its hashes!

Update the "schema_columns" array in the JSON to match your secret dataset's columns (Timestamp, Raw_Value, Auth_Signature).

Open your terminal in the root directory and run:

Bash
python main.py
Sit back and watch the multi-core backpressure do its thing!

[!TIP]
Want to test the Backpressure? Because the PBKDF2 hashing is heavily CPU-intensive, it creates massive bottlenecks. Set "core_parallelism": 1 in the config if you want to see the terminal yell at you in RED instantly. Then set "core_parallelism": 10 to watch the bouncers clear the bottleneck and return the pipeline to GREEN.
