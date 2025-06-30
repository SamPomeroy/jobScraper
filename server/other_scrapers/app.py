# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import asyncio
# import os
# from dotenv import load_dotenv
# from typing import Optional, List
# import uvicorn

# # Import your scraper classes
# from careerindeed import JobScraper, ResumeSkillMatcher

# # Load environment variables
# load_dotenv()

# app = FastAPI(
#     title="Job Scraper API",
#     description="API for scraping jobs from Indeed and CareerBuilder with resume matching",
#     version="1.0.0"
# )

# # Pydantic models for request/response
# class ScrapeRequest(BaseModel):
#     keywords: str = "software developer"
#     location: str = "Remote"
#     pages: int = 2
#     table_name: str = "jobs"

# class ResumeMatchRequest(BaseModel):
#     resume_text: str
#     min_score: float = 0.3
#     limit: int = 10

# class JobResponse(BaseModel):
#     title: str
#     company: str
#     job_location: str
#     job_state: str
#     site: str
#     match_score: Optional[float] = None
#     matching_skills: Optional[List[str]] = None
#     url: str

# @app.get("/")
# async def root():
#     """Root endpoint"""
#     return {
#         "message": "Job Scraper API is running",
#         "endpoints": {
#             "scrape": "/scrape - POST endpoint to scrape jobs",
#             "match": "/match-resume - POST endpoint to match resume with jobs",
#             "health": "/health - Health check endpoint"
#         }
#     }

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     supabase_url = os.getenv("SUPABASE_URL")
#     supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
#     if not supabase_url or not supabase_key:
#         raise HTTPException(status_code=500, detail="Missing Supabase credentials")
    
#     return {"status": "healthy", "database": "connected"}

# @app.post("/scrape")
# async def scrape_jobs(request: ScrapeRequest):
#     """Scrape jobs from Indeed and CareerBuilder"""
    
#     # Check environment variables
#     supabase_url = os.getenv("SUPABASE_URL")
#     supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
#     if not supabase_url or not supabase_key:
#         raise HTTPException(
#             status_code=500, 
#             detail="SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment"
#         )
    
#     try:
#         scraper = JobScraper(str(supabase_url), str(supabase_key))
#         results = await scraper.scrape_and_save(
#             keywords=request.keywords,
#             location=request.location,
#             pages=request.pages,
#             table_name=request.table_name
#         )
        
#         return {
#             "status": "success",
#             "message": f"Successfully scraped {results['total_jobs']} jobs",
#             "results": {
#                 "indeed_jobs": results.get('indeed_jobs', 0),
#                 "careerbuilder_jobs": results.get('careerbuilder_jobs', 0),
#                 "total_jobs": results['total_jobs'],
#                 "csv_file": results.get('csv_file', ''),
#                 "success": results['success']
#             }
#         }
            
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

# @app.post("/match-resume", response_model=List[JobResponse])
# async def match_resume(request: ResumeMatchRequest):
#     """Match resume with jobs in database"""
    
#     # Check environment variables
#     supabase_url = os.getenv("SUPABASE_URL")
#     supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
#     if not supabase_url or not supabase_key:
#         raise HTTPException(
#             status_code=500, 
#             detail="SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment"
#         )
    
#     try:
#         matcher = ResumeSkillMatcher(str(supabase_url), str(supabase_key))
        
#         recommended_jobs = await matcher.get_recommended_jobs(
#             resume_text=request.resume_text,
#             min_score=request.min_score,
#             limit=request.limit
#         )
        
#         # Convert to response format
#         job_responses = []
#         for job in recommended_jobs:
#             job_responses.append(JobResponse(
#                 title=job['title'],
#                 company=job['company'],
#                 job_location=job['job_location'],
#                 job_state=job['job_state'],
#                 site=job['site'],
#                 match_score=job.get('match_score'),
#                 matching_skills=job.get('matching_skills', []),
#                 url=job['url']
#             ))
        
#         return job_responses
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Resume matching failed: {str(e)}")

# @app.post("/scrape-and-match")
# async def scrape_and_match(
#     scrape_request: ScrapeRequest, 
#     resume_text: str,
#     min_score: float = 0.3,
#     limit: int = 10
# ):
#     """Scrape jobs and immediately match with resume"""
    
#     # First scrape jobs
#     scrape_result = await scrape_jobs(scrape_request)
    
#     if scrape_result["status"] != "success":
#         return scrape_result
    
#     # Then match with resume
#     match_request = ResumeMatchRequest(
#         resume_text=resume_text,
#         min_score=min_score,
#         limit=limit
#     )
    
#     try:
#         matched_jobs = await match_resume(match_request)
        
#         return {
#             "status": "success",
#             "scraping_results": scrape_result["results"],
#             "matched_jobs": len(matched_jobs),
#             "jobs": matched_jobs
#         }
        
#     except Exception as e:
#         return {
#             "status": "partial_success",
#             "scraping_results": scrape_result["results"],
#             "matching_error": str(e)
#         }

# # CLI function for direct execution
# async def run_examples():
#     """Run example scraping when file is executed directly"""
#     print("Running Job Scraper Examples...")
    
#     supabase_url = os.getenv("SUPABASE_URL")
#     supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
#     if not supabase_url or not supabase_key:
#         print("Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file")
#         return
    
#     try:
#         # Simple scraping example
#         scraper = JobScraper(str(supabase_url), str(supabase_key))
#         results = await scraper.scrape_and_save(
#             keywords="python developer",
#             location="Remote",
#             pages=1
#         )
        
#         print(f"✅ Scraped {results['total_jobs']} jobs!")
#         print(f"📁 CSV saved as: {results.get('csv_file', 'N/A')}")
#         print(f"💾 Saved to database: {results['success']}")
            
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     # If running directly, run examples
#     asyncio.run(run_examples())
# else:
#     # If imported, just expose the app
#     pass


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