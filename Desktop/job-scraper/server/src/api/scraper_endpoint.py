
# File: backend/src/api/scraper_endpoint.py
import time
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from ..scrapers.crawl4ai_scapper import Crawl4AIJobScraper

app = FastAPI()


class ScrapeRequest(BaseModel):
    user_id: Optional[str] = None
    keywords: Optional[List[str]] = None
    sites: Optional[List[str]] = ["indeed", "linkedin", "glassdoor"]

class ScrapeResponse(BaseModel):
    message: str
    job_id: str
    status: str

# Global scraper instance
scraper = Crawl4AIJobScraper()

@app.post("/api/scrape", response_model=ScrapeResponse)
async def trigger_scrape(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """Trigger job scraping process"""
    try:
        # Run scraping in background
        job_id = f"scrape_{int(time.time())}"
        background_tasks.add_task(run_scrape_task, request.user_id, request.keywords, job_id) # type: ignore
        
        return ScrapeResponse(
            message="Scraping started successfully",
            job_id=job_id,
            status="started"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def run_scrape_task(user_id: str, keywords: List[str], job_id: str):
    """Background task to run scraping"""
    try:
        results = await scraper.run_full_scrape(user_id, keywords)
        print(f"Scraping completed for job {job_id}: {results}")
        
        # Send notification via n8n webhook (implement below)
        # await send_n8n_notification(user_id, results)
        
    except Exception as e:
        print(f"Error in scraping task {job_id}: {e}")
