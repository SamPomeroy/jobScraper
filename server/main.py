from fastapi import FastAPI, Query
from typing import Dict

from app.scraper.indeed_scraper import scrape_indeed
from app.scraper.indeed_crawler import get_jobs_from_crawl4ai
from app.scraper.career_scraper import scrape_careerbuilder
from app.scraper.career_crawler import get_jobs_from_careerbuilder as crawl_cb

from app.utils.file_helpers import write_jobs_to_csv
from app.db.cleanup import cleanup
from app.utils.scan_for_duplicates import scan_for_duplicates

app = FastAPI()

@app.get("/all", summary="Run all scrapers + crawlers + cleanup + dedup + skill enrichment")
def run_all(
    location: str = Query("remote", description="Job location"),
    days: int = Query(15, description="How many days to go back")
) -> Dict:
    print("📦 Scraping Indeed...")
    indeed = scrape_indeed(location, days)

    print("🤖 Deep crawling with Crawl4AI...")
    crawl_indeed = get_jobs_from_crawl4ai(location, days)

    print("🧲 Scraping CareerBuilder...")
    cb = scrape_careerbuilder(location, days)

    print("🕸️ Crawling CareerBuilder...")
    cb_crawl = crawl_cb(location, days)

    all_jobs = indeed + crawl_indeed + cb + cb_crawl
    print(f"\n🗃️ Total jobs collected: {len(all_jobs)}")

    print("📁 Writing to CSV...")
    if all_jobs:
        write_jobs_to_csv(all_jobs, prefix="all_sources")

    print("🧼 Cleaning old and duplicate jobs...")
    cleanup(days)

    print("🧠 Scanning for duplicates...")
    scan_for_duplicates()

    return {
        "indeed_scraped": len(indeed),
        "indeed_crawled": len(crawl_indeed),
        "careerbuilder_scraped": len(cb),
        "careerbuilder_crawled": len(cb_crawl),
        "total_saved": len(all_jobs),
        "status": "✅ All jobs processed successfully!"
    }





# from fastapi import FastAPI, Query
# from typing import Dict

# from app.scraper.indeed_scraper import scrape_indeed
# from app.scraper.indeed_crawler import get_jobs_from_crawl4ai
# from app.scraper.career_scraper import scrape_careerbuilder
# from app.scraper.career_crawler import scrape_careerbuilder as crawl_cb  # if applicable
# from app.db.cleanup import cleanup
# from app.utils.scan_for_duplicates import scan_for_duplicates
# from app.db.connect_database import get_db_connection  # if connection needed

# app = FastAPI()

# @app.get("/all", summary="Run all scrapers and crawlers, cleanup, and deduplication")
# def run_all(location: str = Query("remote"), days: int = Query(15)) -> Dict:
#     print("📦 Scraping Indeed...")
#     indeed = scrape_indeed(location, days)

#     print("🤖 Crawling deeper with Crawl4AI...")
#     crawl_indeed = get_jobs_from_crawl4ai(location, days)

#     print("🔍 Scraping CareerBuilder...")
#     career = scrape_careerbuilder(location)

#     # Optional: Add crawler for CareerBuilder if separate
#     print("🕷️ Crawling CareerBuilder...")
#     crawl_cb_jobs = crawl_cb(location) if crawl_cb else []

#     print("🧹 Running cleanup...")
#     cleanup(days)

#     print("🧠 Scanning for duplicates...")
#     scan_for_duplicates()

#     return {
#         "indeed_scrape": len(indeed),
#         "indeed_crawl": len(crawl_indeed),
#         "careerbuilder_scrape": len(career),
#         "careerbuilder_crawl": len(crawl_cb_jobs),
#         "status": "complete"
#     }