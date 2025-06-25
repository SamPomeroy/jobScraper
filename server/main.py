

# # from app.scraper.indeed_scraper import scrape_jobs  # Adjust the function name as needed
# # # main.py
# # from fastapi import FastAPI


# # app = FastAPI()
# # location = "remote"

# # @app.get("/indeed_scraper")
# # def trigger():
# #     result = scrape_jobs(location, days=30)  # Call the actual function from the module
# #     return {"status": "success", "data": result}



# # main.py

# from fastapi import FastAPI, Query
# from typing import List, Dict

# # import your scraper functions
# from app.scraper.indeed_scraper import scrape_jobs as scrape_indeed
# from app.scraper.career_scraper import scrape_careerbuilder

# app = FastAPI()

# @app.get("/scrape/indeed", summary="Scrape Indeed")
# def run_indeed(
#     location: str = Query("remote", description="Job location"),
#     days: int = Query(30, description="How many days back to search")
# ) -> Dict:
#     """
#     Run the Indeed crawler and return all jobs found.
#     """
#     jobs: List[Dict] = scrape_indeed(location, days)
#     return {
#         "source": "indeed",
#         "count": len(jobs),
#         "jobs": jobs
#     }

# @app.get("/scrape/careerbuilder", summary="Scrape CareerBuilder")
# def run_careerbuilder(
#     location: str = Query("remote", description="Job location"),
#     pages: int = Query(2, description="How many pages to crawl per keyword")
# ) -> Dict:
#     """
#     Run the CareerBuilder crawler and return all jobs found.
#     """
#     jobs: List[Dict] = scrape_careerbuilder(location, pages)
#     return {
#         "source": "careerbuilder",
#         "count": len(jobs),
#         "jobs": jobs
#     }

# @app.get("/scrape/all", summary="Scrape Indeed + CareerBuilder")
# def run_all(
#     location: str = Query("remote", description="Job location"),
#     days: int = Query(30, description="Indeed: days back"),
#     pages: int = Query(2, description="CareerBuilder: pages per keyword")
# ) -> Dict:
#     """
#     Scrape both Indeed and CareerBuilder in one shot.
#     """
#     indeed_jobs = scrape_indeed(location, days)
#     cb_jobs = scrape_careerbuilder(location, pages)

#     return {
#         "indeed": {
#             "count": len(indeed_jobs),
#             "jobs": indeed_jobs
#         },
#         "careerbuilder": {
#             "count": len(cb_jobs),
#             "jobs": cb_jobs
#         }
#     }
    
    
from fastapi import FastAPI, Query
from typing import Dict

from app.scraper.indeed_scraper import scrape_indeed
from app.scraper.career_scraper import scrape_careerbuilder
from app.db.cleanup import cleanup
from app.db.connect_database import get_db_connection
app = FastAPI()

# ─── Endpoint 1: Scrape Indeed ─────────────────────────────────────────────────
@app.get("/indeed", summary="Run the Indeed scraper")
def run_indeed(
    location: str = Query("remote", description="Job location"),
    days:     int = Query(15,      description="How many days back to fetch")
) -> Dict:
    jobs = scrape_indeed(location, days)
    cleanup(days)
    return {"source": "indeed", "count": len(jobs), "jobs": jobs}


# ─── Endpoint 2: Scrape CareerBuilder ──────────────────────────────────────────
@app.get("/careerbuilder", summary="Run the CareerBuilder scraper")
def run_careerbuilder(
    location: str = Query("remote", description="Job location"),
    days:     int = Query(15,      description="How many days back to fetch")
) -> Dict:
    jobs = scrape_careerbuilder(location)
    cleanup(days)
    return {"source": "careerbuilder", "count": len(jobs), "jobs": jobs}


# ─── Endpoint 3: Scrape Both ────────────────────────────────────────────────────
@app.get("/all", summary="Run both scrapers")
def run_all(
    location: str = Query("remote", description="Job location"),
    days:     int = Query(15,      description="How many days back to fetch")
) -> Dict:
    indeed_jobs = scrape_indeed(location, days)
    cb_jobs     = scrape_careerbuilder(location)
    cleanup(days)
    return {
        "indeed":        {"count": len(indeed_jobs)},
        "careerbuilder": {"count": len(cb_jobs)}
    }
@app.get("/")
def root():
    return {"message": "👋 Job Scraper API is running. Use /docs to access endpoints."}