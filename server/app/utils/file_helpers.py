import os
import csv
from datetime import datetime

def write_jobs_to_csv(jobs: list, prefix: str = "jobs"):
    if not jobs:
        print("⚠️ No jobs to write.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", f"{prefix}_{timestamp}.csv")

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        writer.writeheader()
        writer.writerows(jobs)

    print(f"📁 Jobs saved to {filepath}")