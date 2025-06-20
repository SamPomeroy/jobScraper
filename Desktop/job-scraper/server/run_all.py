import subprocess

scripts = [
    "uvicorn utils.main:app --host 0.0.0.0 --port 8000 --reload",
    "python scrapers/crawl4ai_scraper.py",
    "python scrapers/indeed_scraper.py",
]

for script in scripts:
    subprocess.Popen(script, shell=True)