import os

MODE = os.environ.get("MODE", "prod")  # Can be "dev" or "prod"

FOLDERS = {
    "dev": {
        "csv_output": "server/debugged",
        "log_level": "DEBUG"
    },
    "prod": {
        "csv_output": "server/job_data",
        "log_level": "INFO"
    }
}

def get_output_folder():
    return FOLDERS[MODE]["csv_output"]