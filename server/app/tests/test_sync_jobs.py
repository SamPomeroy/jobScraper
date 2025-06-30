import csv
import json
import tempfile
from datetime import date
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.db.sync_jobs import sync_job_data_folder_to_supabase

def create_edge_case_csv(path):
    rows = [
        {
            "title": "",
            "company": "NoName Inc.",
            "job_location": "remote",
            "job_state": "remote",
            "date": str(date.today()),
            "site": "Indeed",
            "job_description": "Missing title",
            "salary": "$80,000",
            "url": "https://test-job-url.com/edge1",
            "applied": "False",
            "search_term": "python",
            "skills": json.dumps(["Python"])
        },
        {
            "title": "Dupe Job",
            "company": "SameCorp",
            "job_location": "remote",
            "job_state": "remote",
            "date": str(date.today()),
            "site": "CareerBuilder",
            "job_description": "Should be skipped if URL duplicate",
            "salary": "$90,000",
            "url": "https://test-job-url.com/edge1",  # same URL as above
            "applied": "False",
            "search_term": "devops",
            "skills": json.dumps(["Docker"])
        }
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def test_sync_job_data_folder_to_supabase():
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, "test_edge_cases.csv")
        create_edge_case_csv(csv_path)

        # Run sync
        sync_job_data_folder_to_supabase(folder=tmpdir)

        # You can also connect to Supabase and assert the job was inserted or skipped
        # For now, just ensuring the function runs without crashing
        assert os.path.exists(csv_path)