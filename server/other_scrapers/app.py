from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import os
import asyncio

# Import your scraper/matcher classes
from server.other_scrapers.careerindeed import JobScraper, ResumeSkillMatcher

# Load .env variables
load_dotenv()

app = FastAPI(
    title="Job Scraper API",
    description="Scrape job listings and match them against a resume using Supabase.",
    version="1.0.0"
)

# 🧱 Pydantic models
class ScrapeRequest(BaseModel):
    keywords: str = "software developer"
    location: str = "Remote"
    pages: int = 2
    table_name: str = "jobs"

class ResumeMatchRequest(BaseModel):
    resume_text: str
    min_score: float = 0.3
    limit: int = 10

class ScrapeAndMatchRequest(ScrapeRequest):
    resume_text: str
    min_score: float = 0.3
    limit: int = 10

class JobResponse(BaseModel):
    title: str
    company: str
    job_location: str
    job_state: str
    site: str
    match_score: Optional[float] = None
    matching_skills: Optional[List[str]] = None
    url: str

# ✅ Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Job Scraper API is running",
        "endpoints": {
            "scrape": "/scrape",
            "match-resume": "/match-resume",
            "scrape-and-match": "/scrape-and-match",
            "health": "/health"
        }
    }

# ✅ Health check
@app.get("/health")
async def health_check():
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_ANON_KEY"):
        raise HTTPException(status_code=500, detail="Supabase credentials not set")
    return {"status": "healthy"}

# 🔍 Scrape jobs only
@app.post("/scrape")
async def scrape_jobs(request: ScrapeRequest):
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    if not supabase_url or not supabase_key:
        raise HTTPException(status_code=500, detail="Missing Supabase credentials")

    try:
        scraper = JobScraper(supabase_url, supabase_key)
        results = await scraper.scrape_and_save(
            keywords=request.keywords,
            location=request.location,
            pages=request.pages,
            table_name=request.table_name
        )
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scrape failed: {str(e)}")

# 🧠 Resume matcher only
@app.post("/match-resume", response_model=List[JobResponse])
async def match_resume(request: ResumeMatchRequest):
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    if not supabase_url or not supabase_key:
        raise HTTPException(status_code=500, detail="Missing Supabase credentials")

    try:
        matcher = ResumeSkillMatcher(supabase_url, supabase_key)
        matched = await matcher.get_recommended_jobs(
            resume_text=request.resume_text,
            min_score=request.min_score,
            limit=request.limit
        )
        return [
            JobResponse(
                title=job["title"],
                company=job["company"],
                job_location=job["job_location"],
                job_state=job["job_state"],
                site=job["site"],
                match_score=job.get("match_score"),
                matching_skills=job.get("matching_skills", []),
                url=job["url"]
            ) for job in matched
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")

# 🔄 Scrape + Match combo (perfect for n8n!)
@app.post("/scrape-and-match")
async def scrape_and_match(payload: ScrapeAndMatchRequest):
    try:
        scraping = await scrape_jobs(payload)
        if scraping["status"] != "success":
            raise Exception("Scraping failed.")

        match_request = ResumeMatchRequest(
            resume_text=payload.resume_text,
            min_score=payload.min_score,
            limit=payload.limit
        )
        jobs = await match_resume(match_request)
        return {
            "status": "success",
            "scraping_results": scraping["results"],
            "matched_jobs": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }

# Optional CLI for local test runs
async def run_examples():
    print("Running example job scrape + match...")
    scrape_req = ScrapeRequest(keywords="python", location="Remote", pages=1)
    resume = "Experienced Python developer with background in REST APIs and cloud services..."
    match_req = ResumeMatchRequest(resume_text=resume)

    scrape_response = await scrape_jobs(scrape_req)
    match_response = await match_resume(match_req)
    print("Scraped:", scrape_response)
    print("Matched:", match_response)

if __name__ == "__main__":
    asyncio.run(run_examples())