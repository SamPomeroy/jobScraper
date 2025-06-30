from fastapi import FastAPI, Query, HTTPException, Header
from typing import Dict
from pydantic import BaseModel
import os
from jose import jwt, JWTError

from app.scraper.indeed_scraper import scrape_indeed
from app.scraper.indeed_crawler import get_jobs_from_crawl4ai
from app.scraper.career_scraper import scrape_careerbuilder
from app.scraper.career_crawler import get_jobs_from_careerbuilder as crawl_cb

from app.db.connect_database import supabase
from app.db.cleanup import cleanup
from app.utils.scan_for_duplicates import scan_for_duplicates
from app.utils.write_jobs import write_jobs_csv
from app.db.sync_jobs import sync_job_data_folder_to_supabase
from app.config.config_utils import get_output_folder

from app.services.skills_loader import load_all_skills
from app.services.skills import extract_skills_by_category
from app.utils.skill_utils import extract_flat_skills

app = FastAPI()
SKILLS = load_all_skills()  # 🔁 Load once at startup

class JobDesc(BaseModel):
    text: str

def get_current_user_id(authorization: str = Header(...)) -> str:
    token = authorization.replace("Bearer ", "")
    secret = os.environ["SUPABASE_JWT_SECRET"]
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid auth token")


@app.post("/flat-skills/extract")
def flat_skill_extract(payload: JobDesc):
    flat = extract_flat_skills(payload.text, SKILLS["flat"])
    categorized = extract_skills_by_category(payload.text, SKILLS["matrix"])
    return {
        "flat_skills": flat,
        "skills_by_category": categorized
    }


@app.get("/indeed", summary="Scrape and crawl Indeed")
def run_indeed(
    location: str = Query("remote"),
    days: int = Query(15),
    debug: bool = Query(False)
) -> Dict:
    print("📦 Scraping Indeed...")
    indeed = scrape_indeed(location, days)

    print("🤖 Crawling deeper with Crawl4AI...")
    crawl_indeed = get_jobs_from_crawl4ai(location, days)

    folder = get_output_folder()
    write_jobs_csv(indeed, folder_name=folder, label="indeed_scrape")
    write_jobs_csv(crawl_indeed, folder_name=folder, label="indeed_crawl")

    return {
        "indeed_scrape": len(indeed),
        "indeed_crawl": len(crawl_indeed),
        "status": "indeed complete"
    }


@app.get("/careerbuilder", summary="Scrape and crawl CareerBuilder")
def run_careerbuilder(
    location: str = Query("remote"),
    days: int = Query(15),
    debug: bool = Query(False)
) -> Dict:
    print("🔍 Scraping CareerBuilder...")
    career = scrape_careerbuilder(location)

    print("🕷️ Crawling CareerBuilder...")
    crawl_cb_jobs = crawl_cb(location) if crawl_cb else []

    folder = get_output_folder()
    write_jobs_csv(career, folder_name=folder, label="career_scrape")
    write_jobs_csv(crawl_cb_jobs, folder_name=folder, label="career_crawl")

    return {
        "careerbuilder_scrape": len(career),
        "careerbuilder_crawl": len(crawl_cb_jobs),
        "status": "careerbuilder complete"
    }


@app.get("/all", summary="Run scrapers, enrich skills, cleanup, and Supabase sync")
def run_all(
    location: str = Query("remote"),
    days: int = Query(15),
    debug: bool = Query(False),
    secret: str = Query(...)
) -> Dict:
    if secret != os.getenv("SCRAPER_SECRET_TOKEN"):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

    print("📦 Scraping Indeed...")
    indeed = scrape_indeed(location, days)

    print("🤖 Crawling Indeed with Crawl4AI...")
    crawl_indeed = get_jobs_from_crawl4ai(location, days)

    print("🔍 Scraping CareerBuilder...")
    career = scrape_careerbuilder(location)

    print("🕷️ Crawling CareerBuilder...")
    crawl_cb_jobs = crawl_cb(location) if crawl_cb else []

    # 🔎 Enrich all jobs with skills
    for job_list in [indeed, crawl_indeed, career, crawl_cb_jobs]:
        for job in job_list:
            text = f"{job.get('title', '')} {job.get('job_description', '')}"
            job["flat_skills"] = extract_flat_skills(text, SKILLS["flat"])
            job["skills_by_category"] = extract_skills_by_category(text, SKILLS["matrix"])

    folder = get_output_folder()
    print(f"💾 Output to folder: {folder}")

    write_jobs_csv(indeed, folder_name=folder, label="indeed_scrape")
    write_jobs_csv(crawl_indeed, folder_name=folder, label="indeed_crawl")
    write_jobs_csv(career, folder_name=folder, label="career_scrape")
    write_jobs_csv(crawl_cb_jobs, folder_name=folder, label="career_crawl")

    print("🧹 Running cleanup...")
    cleanup(days)

    print("🧠 Scanning for duplicates...")
    scan_for_duplicates()

    print("📤 Syncing to Supabase...")
    sync_job_data_folder_to_supabase(folder=folder)

    return {
        "indeed_scrape": len(indeed),
        "indeed_crawl": len(crawl_indeed),
        "careerbuilder_scrape": len(career),
        "careerbuilder_crawl": len(crawl_cb_jobs),
        "status": "All jobs scraped, enriched, deduped, and synced to Supabase"
    }


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/job-action")
def job_action_get_user_id(authorization: str = Header(...)) -> str:
    token = authorization.replace("Bearer ", "")
    secret = os.environ["SUPABASE_JWT_SECRET"]
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid auth token")

# from fastapi import FastAPI, Query, HTTPException, Header
# from typing import Dict
# from pydantic import BaseModel
# import os
# from jose import jwt, JWTError

# from app.scraper.indeed_scraper import scrape_indeed
# from app.scraper.indeed_crawler import get_jobs_from_crawl4ai
# from app.scraper.career_scraper import scrape_careerbuilder
# from app.scraper.career_crawler import get_jobs_from_careerbuilder as crawl_cb

# from app.db.connect_database import supabase
# from app.db.cleanup import cleanup
# from app.utils.scan_for_duplicates import scan_for_duplicates
# from app.utils.write_jobs import write_jobs_csv
# from app.db.sync_jobs import sync_job_data_folder_to_supabase

# from app.config.config_utils import get_output_folder

# from app.services.skills_loader import load_all_skills
# from app.services.skills import extract_skills_by_category
# from app.utils.skill_utils import extract_flat_skills

# app = FastAPI()

# # Load skills once at app startup
# SKILLS = load_all_skills()

# class JobDesc(BaseModel):
#     text: str

# def get_current_user_id(authorization: str = Header(...)) -> str:
#     token = authorization.replace("Bearer ", "")
#     secret = os.environ["SUPABASE_JWT_SECRET"]
#     try:
#         payload = jwt.decode(token, secret, algorithms=["HS256"])
#         return payload["sub"]
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid auth token")


# @app.post("/flat-skills/extract")
# def flat_skill_extract(payload: JobDesc):
#     flat = extract_flat_skills(payload.text, SKILLS["flat"])
#     categorized = extract_skills_by_category(payload.text, SKILLS["matrix"])
#     return {
#         "flat_skills": flat,
#         "skills_by_category": categorized
#     }


# @app.get("/indeed", summary="Scrape and crawl Indeed")
# def run_indeed(
#     location: str = Query("remote"),
#     days: int = Query(15),
#     debug: bool = Query(False)
# ) -> Dict:
#     print("📦 Scraping Indeed...")
#     indeed = scrape_indeed(location, days)

#     print("🤖 Crawling deeper with Crawl4AI...")
#     crawl_indeed = get_jobs_from_crawl4ai(location, days)

#     folder = get_output_folder()
#     write_jobs_csv(indeed, folder_name=folder, label="indeed_scrape")
#     write_jobs_csv(crawl_indeed, folder_name=folder, label="indeed_crawl")

#     return {
#         "indeed_scrape": len(indeed),
#         "indeed_crawl": len(crawl_indeed),
#         "status": "indeed complete"
#     }


# @app.get("/careerbuilder", summary="Scrape and crawl CareerBuilder")
# def run_careerbuilder(
#     location: str = Query("remote"),
#     days: int = Query(15),
#     debug: bool = Query(False)
# ) -> Dict:
#     print("🔍 Scraping CareerBuilder...")
#     career = scrape_careerbuilder(location)

#     print("🕷️ Crawling CareerBuilder...")
#     crawl_cb_jobs = crawl_cb(location) if crawl_cb else []

#     folder = get_output_folder()
#     write_jobs_csv(career, folder_name=folder, label="career_scrape")
#     write_jobs_csv(crawl_cb_jobs, folder_name=folder, label="career_crawl")

#     return {
#         "careerbuilder_scrape": len(career),
#         "careerbuilder_crawl": len(crawl_cb_jobs),
#         "status": "careerbuilder complete"
#     }


# @app.get("/all", summary="Run scrapers, cleanup, deduplication, and Supabase sync")
# def run_all(
#     location: str = Query("remote"),
#     days: int = Query(15),
#     debug: bool = Query(False),
#     secret: str = Query(...)
# ) -> Dict:
#     expected_secret = os.getenv("SCRAPER_SECRET_TOKEN")
#     if secret != expected_secret:
#         raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

#     print("📦 Scraping Indeed...")
#     indeed = scrape_indeed(location, days)

#     print("🤖 Crawling Indeed with Crawl4AI...")
#     crawl_indeed = get_jobs_from_crawl4ai(location, days)

#     print("🔍 Scraping CareerBuilder...")
#     career = scrape_careerbuilder(location)

#     print("🕷️ Crawling CareerBuilder...")
#     crawl_cb_jobs = crawl_cb(location) if crawl_cb else []

#     folder = get_output_folder()
#     print(f"💾 Output to folder: {folder}")

#     write_jobs_csv(indeed, folder_name=folder, label="indeed_scrape")
#     write_jobs_csv(crawl_indeed, folder_name=folder, label="indeed_crawl")
#     write_jobs_csv(career, folder_name=folder, label="career_scrape")
#     write_jobs_csv(crawl_cb_jobs, folder_name=folder, label="career_crawl")

#     print("🧹 Running cleanup...")
#     cleanup(days)

#     print("🧠 Scanning for duplicates...")
#     scan_for_duplicates()

#     print("📤 Syncing to Supabase...")
#     sync_job_data_folder_to_supabase(folder=folder)

#     return {
#         "indeed_scrape": len(indeed),
#         "indeed_crawl": len(crawl_indeed),
#         "careerbuilder_scrape": len(career),
#         "careerbuilder_crawl": len(crawl_cb_jobs),
#         "status": "All jobs scraped, deduped, and synced to Supabase"
#     }


# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}


# @app.post("/job-action")
# def job_action_get_user_id(authorization: str = Header(...)) -> str:
#     token = authorization.replace("Bearer ", "")
#     secret = os.environ["SUPABASE_JWT_SECRET"]
#     try:
#         payload = jwt.decode(token, secret, algorithms=["HS256"])
#         return payload["sub"]
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid auth token")



# from fastapi import FastAPI, Query, HTTPException, Depends,Header
# from typing import Dict
# from app.scraper.indeed_scraper import scrape_indeed
# from jose import jwt, JWTError
# import os
# from app.scraper.indeed_crawler import get_jobs_from_crawl4ai
# from app.scraper.career_scraper import scrape_careerbuilder
# from app.scraper.career_crawler import get_jobs_from_careerbuilder as crawl_cb  # if applicable
# from app.db.cleanup import cleanup
# from app.utils.scan_for_duplicates import scan_for_duplicates
# from app.db.connect_database import get_db_connection 
# from app.utils.write_jobs import write_jobs_csv
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.config.config_utils import get_output_folder
# from pydantic import BaseModel
# from app.utils.skill_utils import load_flat_skills, extract_flat_skills
# def get_current_user_id(authorization: str = Header(...)) -> str:
#     token = authorization.replace("Bearer ", "")
#     secret = os.environ["SUPABASE_JWT_SECRET"]
#     try:
#         payload = jwt.decode(token, secret, algorithms=["HS256"])
#         return payload["sub"]  # Supabase stores user ID in 'sub'
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid auth token")
# skill_list = load_flat_skills("app/resources/skills.txt")
# FLAT_SKILL_LIST = load_flat_skills("app/resources/skills.txt")
# app = FastAPI()
# class JobDesc(BaseModel):
#     text: str
# @app.post("/flat-skills/extract")
# def flat_skill_extract(payload: JobDesc):
#     extracted = extract_flat_skills(payload.text, FLAT_SKILL_LIST)
#     return {"skills": extracted}



# @app.get("/indeed", summary="Scrape and crawl Indeed")
# def run_indeed(
#     location: str = Query("remote"),
#     days: int = Query(15),
#     debug: bool = Query(False)
# ) -> Dict:


#     print("📦 Scraping Indeed...")
#     indeed = scrape_indeed(location, days)

#     print("🤖 Crawling deeper with Crawl4AI...")
#     crawl_indeed = get_jobs_from_crawl4ai(location, days)

#     folder = get_output_folder()


#     # folder = "debugged" if debug else "job_data"
#     write_jobs_csv(indeed, folder_name=folder, label="indeed_scrape")
#     write_jobs_csv(crawl_indeed, folder_name=folder, label="indeed_crawl")

#     return {
#         "indeed_scrape": len(indeed),
#         "indeed_crawl": len(crawl_indeed),
#         "status": "indeed complete"
#     }


# @app.get("/careerbuilder", summary="Scrape and crawl CareerBuilder")
# def run_careerbuilder(location: str = Query("remote"), days: int = Query(15), debug: bool = Query(False)) -> Dict:
#     print("🔍 Scraping CareerBuilder...")
#     career = scrape_careerbuilder(location)

#     print("🕷️ Crawling CareerBuilder...")
#     crawl_cb_jobs = crawl_cb(location) if crawl_cb else []
#     folder = get_output_folder()

#     # folder = "debugged" if debug else "job_data"
#     write_jobs_csv(career, folder_name=folder, label="career_scrape")
#     write_jobs_csv(crawl_cb_jobs, folder_name=folder, label="career_crawl")

#     return {
#         "careerbuilder_scrape": len(career),
#         "careerbuilder_crawl": len(crawl_cb_jobs),
#         "status": "careerbuilder complete"
#     }
# from app.db.connect_database import supabase
# @app.get("/all", summary="Run scrapers, cleanup, deduplication, and Supabase sync")
# def run_all(
#     location: str = Query("remote"),
#     days: int = Query(15),
#     debug: bool = Query(False),
#     secret: str = Query(...)
# ) -> Dict:
#     # 🔐 Token validation
#     expected_secret = os.getenv("SCRAPER_SECRET_TOKEN")
#     if secret != expected_secret:
#         raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

#     print("📦 Scraping Indeed...")
#     indeed = scrape_indeed(location, days)

#     print("🤖 Crawling Indeed with Crawl4AI...")
#     crawl_indeed = get_jobs_from_crawl4ai(location, days)

#     print("🔍 Scraping CareerBuilder...")
#     career = scrape_careerbuilder(location)

#     print("🕷️ Crawling CareerBuilder...")
#     crawl_cb_jobs = crawl_cb(location) if crawl_cb else []

#     folder = get_output_folder()
#     print(f"💾 Output to folder: {folder}")
#     write_jobs_csv(indeed, folder_name=folder, label="indeed_scrape")
#     write_jobs_csv(crawl_indeed, folder_name=folder, label="indeed_crawl")
#     write_jobs_csv(career, folder_name=folder, label="career_scrape")
#     write_jobs_csv(crawl_cb_jobs, folder_name=folder, label="career_crawl")

#     print("🧹 Running cleanup...")
#     cleanup(days)

#     print("🧠 Scanning for duplicates...")
#     scan_for_duplicates()

#     print("📤 Syncing to Supabase...")
#     sync_job_data_folder_to_supabase(folder=folder)

#     return {
#         "indeed_scrape": len(indeed),
#         "indeed_crawl": len(crawl_indeed),
#         "careerbuilder_scrape": len(career),
#         "careerbuilder_crawl": len(crawl_cb_jobs),
#         "status": "All jobs scraped, deduped, and synced to Supabase"
#     }
# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}
# @app.post("/job-action")
# def job_action_get_user_id(authorization: str = Header(...)) -> str:
#     token = authorization.replace("Bearer ", "")
#     secret = os.environ["SUPABASE_JWT_SECRET"]
#     try:
#         payload = jwt.decode(token, secret, algorithms=["HS256"])
#         return payload["sub"]  # Supabase stores user ID in 'sub'
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid auth token")


# @app.get("/cleanup")
# def run_cleanup(days: int = Query(15)) -> Dict:
#     cleanup(days)
#     return {"status": "cleanup complete"}

# @app.get("/dedupe")
# def run_dedupe() -> Dict:
#     scan_for_duplicates()
#     return {"status": "deduplication complete"}



# @app.get("/resync", summary="Resync job_data or debugged CSVs to Supabase")
# def run_resync() -> Dict:
#     folder = get_output_folder()
#     sync_job_data_folder_to_supabase(folder=folder)
#     return {"status": f"resynced CSVs from {folder}"}


# from fastapi import FastAPI, Query
# from typing import Dict

# from app.scraper.indeed_scraper import scrape_indeed
# from app.scraper.indeed_crawler import get_jobs_from_crawl4ai
# from app.scraper.career_scraper import scrape_careerbuilder
# from app.scraper.career_crawler import get_jobs_from_careerbuilder as crawl_cb

# from app.utils.file_helpers import write_jobs_to_csv
# from app.db.cleanup import cleanup
# from app.utils.scan_for_duplicates import scan_for_duplicates

# app = FastAPI()

# @app.get("/all", summary="Run all scrapers + crawlers + cleanup + dedup + skill enrichment")
# def run_all(
#     location: str = Query("remote", description="Job location"),
#     days: int = Query(15, description="How many days to go back")
# ) -> Dict:
#     print("📦 Scraping Indeed...")
#     indeed = scrape_indeed(location, days)

#     print("🤖 Deep crawling with Crawl4AI...")
#     crawl_indeed = get_jobs_from_crawl4ai(location, days)

#     print("🧲 Scraping CareerBuilder...")
#     cb = scrape_careerbuilder(location, days)

#     print("🕸️ Crawling CareerBuilder...")
#     cb_crawl = crawl_cb(location, days)

#     all_jobs = indeed + crawl_indeed + cb + cb_crawl
#     print(f"\n🗃️ Total jobs collected: {len(all_jobs)}")

#     print("📁 Writing to CSV...")
#     if all_jobs:
#         write_jobs_to_csv(all_jobs, prefix="all_sources")

#     print("🧼 Cleaning old and duplicate jobs...")
#     cleanup(days)

#     print("🧠 Scanning for duplicates...")
#     scan_for_duplicates()

#     return {
#         "indeed_scraped": len(indeed),
#         "indeed_crawled": len(crawl_indeed),
#         "careerbuilder_scraped": len(cb),
#         "careerbuilder_crawled": len(cb_crawl),
#         "total_saved": len(all_jobs),
#         "status": "✅ All jobs processed successfully!"
#     }
