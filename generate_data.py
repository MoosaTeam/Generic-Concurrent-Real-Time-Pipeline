import os
import csv
import random

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)
filepath = "data/unseen_climate_data.csv"

countries = ["Senegal", "Canada", "Japan", "Brazil", "Germany"]

print(f"Generating rows of test data at {filepath}...")
with open(filepath, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # These headers MUST match your config.json source_names exactly
    writer.writerow(["Country Name", "Year", "Average_Temperature_C", "Ignore_This_Column"])
    
    for i in range(300):
        country = random.choice(countries)
        year = 2026 - (i % 50)
        temp = round(random.uniform(-10.0, 45.0), 2)
        writer.writerow([country, year, temp, "garbage_data"])

print("Data generation complete.")
