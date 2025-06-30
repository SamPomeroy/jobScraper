from pathlib import Path
from datetime import datetime
import csv

def write_jobs_csv(jobs: list, folder_name: str = "job_data", label: str = "careerbuilder"):
    if not jobs:
        return

    # Make path relative to the script root, not hardcoded "server/"
    path = Path(__file__).resolve().parent.parent / folder_name
    path.mkdir(parents=True, exist_ok=True)

    filename = path / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(jobs[0].keys()))
        writer.writeheader()
        writer.writerows(jobs)

    print(f"📁 CSV saved to {filename}")