from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import json
import os
from datetime import datetime
import uuid
import io
import docx
import PyPDF2
from supabase import create_client, Client
import logging

# Import our scraper classes
from server.other_scrapers.careerindeed import JobScraper, ResumeSkillMatcher, SkillExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Job Recommendation API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "your-supabase-url")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-supabase-key")
SKILLS_FILE_PATH = os.getenv("SKILLS_FILE_PATH", "utils/skills.json")

# Initialize services
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
skill_matcher = ResumeSkillMatcher(SUPABASE_URL, SUPABASE_KEY, SKILLS_FILE_PATH)


# Pydantic models
class JobRecommendationRequest(BaseModel):
    resume_text: str
    min_score: float = 0.2
    limit: int = 50
    user_id: Optional[str] = None


class JobRecommendationResponse(BaseModel):
    success: bool
    total_jobs: int
    recommendations: List[Dict]
    resume_skills: List[str]
    message: str


class ScrapingRequest(BaseModel):
    keywords: str
    location: str = ""
    pages: int = 5
    user_id: Optional[str] = None


class ScrapingResponse(BaseModel):
    success: bool
    indeed_jobs: int
    careerbuilder_jobs: int
    total_jobs: int
    duplicates_skipped: int
    csv_file: str
    message: str


class ResumeUploadResponse(BaseModel):
    success: bool
    extracted_text: str
    extracted_skills: List[str]
    message: str


# Utility functions
def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file."""
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        return ""


def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from TXT file."""
    try:
        return file_content.decode('utf-8').strip()
    except Exception as e:
        logger.error(f"Error extracting text from TXT: {e}")
        return ""


async def extract_text_from_resume(file: UploadFile) -> str:
    """Extract text from resume file based on file type."""
    content = await file.read()
    
    if file.content_type == "application/pdf":
        return extract_text_from_pdf(content)
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(content)
    elif file.content_type == "text/plain":
        return extract_text_from_txt(content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF, DOCX, or TXT files.")


# Background task for scraping
async def run_scraping_task(keywords: str, location: str, pages: int, user_id: Optional[str] = None):
    """Background task to run job scraping."""
    try:
        async with JobScraper(SUPABASE_URL, SUPABASE_KEY, SKILLS_FILE_PATH) as scraper:
            results = await scraper.scrape_and_save(
                keywords=keywords,
                location=location,
                pages=pages,
                table_name='jobs'
            )
            
            # Update jobs with user_id if provided
            if user_id and results.get('success'):
                try:
                    supabase.table('jobs').update({'user_id': user_id}).eq('user_id', None).execute()
                except Exception as e:
                    logger.error(f"Error updating user_id: {e}")
            
            logger.info(f"Background scraping completed: {results}")
            
    except Exception as e:
        logger.error(f"Background scraping failed: {e}")


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Job Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "upload_resume": "/upload-resume",
            "get_recommendations": "/recommendations",
            "start_scraping": "/scrape-jobs",
            "get_jobs": "/jobs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test Supabase connection
        result = supabase.table('jobs').select('count').execute()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@app.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and process a resume file to extract text and skills.
    Supports PDF, DOCX, and TXT files.
    """
    try:
        # Validate file type
        allowed_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain"
        ]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload PDF, DOCX, or TXT files."
            )
        
        # Extract text from resume
        extracted_text = await extract_text_from_resume(file)
        
        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the uploaded file."
            )
        
        # Extract skills from resume text
        extracted_skills = skill_matcher.extract_skills_from_resume(extracted_text)
        
        return ResumeUploadResponse(
            success=True,
            extracted_text=extracted_text,
            extracted_skills=extracted_skills,
            message=f"Successfully processed resume. Found {len(extracted_skills)} matching skills."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        raise HTTPException(status_code=500, detail="Internal server error processing resume.")


@app.post("/recommendations", response_model=JobRecommendationResponse)
async def get_job_recommendations(request: JobRecommendationRequest):
    """
    Get job recommendations based on resume text and skills.
    """
    try:
        # Get recommended jobs
        recommendations = await skill_matcher.get_recommended_jobs(
            resume_text=request.resume_text,
            min_score=request.min_score,
            limit=request.limit,
            user_id=request.user_id
        )
        
        # Extract skills from resume
        resume_skills = skill_matcher.extract_skills_from_resume(request.resume_text)
        
        return JobRecommendationResponse(
            success=True,
            total_jobs=len(recommendations),
            recommendations=recommendations,
            resume_skills=resume_skills,
            message=f"Found {len(recommendations)} job recommendations with minimum score {request.min_score}"
        )
        
    except Exception as e:
        logger.error(f"Error getting job recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error getting recommendations.")


@app.post("/scrape-jobs", response_model=ScrapingResponse)
async def start_job_scraping(request: ScrapingRequest, background_tasks: BackgroundTasks):
    """
    Start job scraping process in the background.
    Returns immediately with a task ID.
    """
    try:
        # Add scraping task to background tasks
        background_tasks.add_task(
            run_scraping_task,
            keywords=request.keywords,
            location=request.location,
            pages=request.pages,
            user_id=request.user_id
        )
        
        return ScrapingResponse(
            success=True,
            indeed_jobs=0,
            careerbuilder_jobs=0,
            total_jobs=0,
            duplicates_skipped=0,
            csv_file="Will be generated during scraping",
            message=f"Scraping started for '{request.keywords}' in '{request.location}'. Check back in a few minutes."
        )
        
    except Exception as e:
        logger.error(f"Error starting scraping: {e}")
        raise HTTPException(status_code=500, detail="Internal server error starting scraping.")


@app.get("/jobs")
async def get_jobs(
    user_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    search_term: Optional[str] = None,
    location: Optional[str] = None,
    site: Optional[str] = None
):
    """
    Get jobs from the database with optional filtering.
    """
    try:
        query = supabase.table('jobs').select('*')
        
        # Apply filters
        if user_id:
            query = query.eq('user_id', user_id)
        if search_term:
            query = query.eq('search_term', search_term)
        if location:
            query = query.ilike('job_location', f'%{location}%')
        if site:
            query = query.eq('site', site)
        
        # Apply pagination
        query = query.range(offset, offset + limit - 1)
        
        # Order by most recent
        query = query.order('inserted_at', desc=True)
        
        result = query.execute()
        
        return {
            "success": True,
            "total": len(result.data),
            "jobs": result.data,
            "offset": offset,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error getting jobs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error getting jobs.")


@app.get("/jobs/{job_id}")
async def get_job_by_id(job_id: str):
    """Get a specific job by ID."""
    try:
        result = supabase.table('jobs').select('*').eq('id', job_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Job not found.")
        
        return {
            "success": True,
            "job": result.data[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job by ID: {e}")
        raise HTTPException(status_code=500, detail="Internal server error getting job.")


@app.put("/jobs/{job_id}")
async def update_job(job_id: str, updates: Dict):
    """Update a job's status, priority, or other fields."""
    try:
        # Only allow certain fields to be updated
        allowed_fields = ['applied', 'priority', 'status', 'category', 'user_id']
        filtered_updates = {k: v for k, v in updates.items() if k in allowed_fields}
        
        if not filtered_updates:
            raise HTTPException(status_code=400, detail="No valid fields to update.")
        
        filtered_updates['last_verified'] = datetime.utcnow().isoformat()
        
        result = supabase.table('jobs').update(filtered_updates).eq('id', job_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Job not found.")
        
        return {
            "success": True,
            "message": "Job updated successfully",
            "job": result.data[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error updating job.")


@app.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a job by ID."""
    try:
        result = supabase.table('jobs').delete().eq('id', job_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Job not found.")
        
        return {
            "success": True,
            "message": "Job deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error deleting job.")


@app.get("/skills")
async def get_available_skills():
    """Get the list of available skills for matching."""
    try:
        skill_extractor = SkillExtractor(SKILLS_FILE_PATH)
        return {
            "success": True,
            "total_skills": len(skill_extractor.skills),
            "skills": skill_extractor.skills
        }
        
    except Exception as e:
        logger.error(f"Error getting skills: {e}")
        raise HTTPException(status_code=500, detail="Internal server error getting skills.")


@app.get("/stats")
async def get_statistics(user_id: Optional[str] = None):
    """Get database statistics."""
    try:
        query = supabase.table('jobs').select('*')
        if user_id:
            query = query.eq('user_id', user_id)
        
        result = query.execute()
        jobs = result.data
        
        stats = {
            "total_jobs": len(jobs),
            "jobs_by_site": {},
            "jobs_by_status": {},
            "applied_jobs": 0,
            "recent_jobs": 0  # Jobs from last 7 days
        }
        
        # Calculate statistics
        from datetime import timedelta
        recent_date = datetime.utcnow() - timedelta(days=7)
        
        for job in jobs:
            # Count by site
            site = job.get('site', 'Unknown')
            stats["jobs_by_site"][site] = stats["jobs_by_site"].get(site, 0) + 1
            
            # Count by status
            status = job.get('status', 'new')
            stats["jobs_by_status"][status] = stats["jobs_by_status"].get(status, 0) + 1
            
            # Count applied jobs
            if job.get('applied', False):
                stats["applied_jobs"] += 1
            
            # Count recent jobs
            if job.get('inserted_at'):
                try:
                    job_date = datetime.fromisoformat(job['inserted_at'].replace('Z', '+00:00'))
                    if job_date > recent_date:
                        stats["recent_jobs"] += 1
                except:
                    pass
        
        return {
            "success": True,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error getting statistics.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)