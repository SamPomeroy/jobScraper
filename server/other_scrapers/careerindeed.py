import asyncio
import json
import re
import csv
import uuid
from datetime import datetime, date
from typing import List, Dict, Optional, Set, Any, Union
from urllib.parse import urlencode, urlparse
import os
from pathlib import Path
from supabase import create_client
import os
from dotenv import load_dotenv

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from supabase import create_client, Client
import logging
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

supabase = create_client(url, key)
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkillExtractor:
    def __init__(self, skills_file_path: str = "utils/skills.json"):
        """
        Initialize skill extractor with skills from file.
        
        Args:
            skills_file_path: Path to skills JSON file
        """
        self.skills = self.load_skills(skills_file_path)
        self.skills_lower = [skill.lower() for skill in self.skills]
        
    def load_skills(self, file_path: str) -> List[str]:
        """Load skills from JSON file."""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle different JSON structures
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict):
                        return data.get('skills', [])
            else:
                logger.warning(f"Skills file not found: {file_path}")
                return self.get_default_skills()
        except Exception as e:
            logger.error(f"Error loading skills file: {e}")
            return self.get_default_skills()
        
        # This return ensures all code paths return a value
        return self.get_default_skills()
    
    def get_default_skills(self) -> List[str]:
        """Return default skills list if file not found."""
        return [
            "Python", "JavaScript", "Java", "C++", "C#", "HTML", "CSS", "React", 
            "Node.js", "Django", "Flask", "Spring", "Angular", "Vue.js", "SQL", 
            "MongoDB", "PostgreSQL", "MySQL", "Git", "Docker", "Kubernetes", 
            "AWS", "Azure", "GCP", "Linux", "Windows", "MacOS", "Agile", "Scrum",
            "Machine Learning", "AI", "Data Science", "Pandas", "NumPy", "TensorFlow",
            "PyTorch", "REST API", "GraphQL", "Microservices", "CI/CD", "Jenkins",
            "Terraform", "Ansible", "Redis", "Elasticsearch", "Kafka", "RabbitMQ"
        ]
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from job description text."""
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skills:
            skill_lower = skill.lower()
            
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates


class JobScraper:
    def __init__(self, supabase_url: str, supabase_key: str, skills_file_path: str = "utils/skills.json"):
        """
        Initialize the job scraper with Supabase credentials and skill extractor.
        
        Args:
            supabase_url: Your Supabase project URL
            supabase_key: Your Supabase anon/service key
            skills_file_path: Path to skills JSON file
        """
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.crawler: Optional[AsyncWebCrawler] = None
        self.skill_extractor = SkillExtractor(skills_file_path)
        self.existing_jobs: Set[str] = set()
        self.csv_filename = f"scraped_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.crawler = AsyncWebCrawler(verbose=True)
        await self.crawler.__aenter__()
        await self.load_existing_jobs()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.crawler:
            await self.crawler.__aexit__(exc_type, exc_val, exc_tb)
    
    async def load_existing_jobs(self):
        """Load existing job URLs from database to prevent duplicates."""
        try:
            result = self.supabase.table('jobs').select('url').execute()
            self.existing_jobs = {job['url'] for job in result.data if job.get('url')}
            logger.info(f"Loaded {len(self.existing_jobs)} existing job URLs for duplicate detection")
        except Exception as e:
            logger.error(f"Error loading existing jobs: {e}")
            self.existing_jobs = set()
    
    def build_indeed_search_url(self, keywords: str, location: str = "", 
                               start: int = 0, limit: int = 50) -> str:
        """Build Indeed search URL with parameters."""
        base_url = "https://www.indeed.com/jobs"
        params = {
            'q': keywords,
            'l': location,
            'start': start,
            'limit': limit
        }
        return f"{base_url}?{urlencode(params)}"
    
    def build_careerbuilder_search_url(self, keywords: str, location: str = "", 
                                     page: int = 1) -> str:
        """Build CareerBuilder search URL with parameters."""
        base_url = "https://www.careerbuilder.com/jobs"
        params = {
            'keywords': keywords,
            'location': location,
            'page_number': page
        }
        return f"{base_url}?{urlencode(params)}"
    
    async def scrape_indeed_jobs(self, keywords: str, location: str = "", 
                               pages: int = 5) -> List[Dict]:
        """Scrape job listings from Indeed."""
        jobs = []
        
        if not self.crawler:
            logger.error("Crawler not initialized")
            return jobs
        
        for page in range(pages):
            start = page * 10
            url = self.build_indeed_search_url(keywords, location, start)
            
            logger.info(f"Scraping Indeed page {page + 1}: {url}")
            
            try:
                # Create extraction strategy as a proper ExtractionStrategy object
                extraction_strategy = {
                    "type": "css_extractor",
                    "params": {
                        "job_cards": {
                            "selector": "[data-jk]",
                            "fields": {
                                "job_id": {"selector": "[data-jk]", "attribute": "data-jk"},
                                "title": {"selector": "h2 a span", "attribute": "title"},
                                "company": {"selector": "[data-testid='company-name']"},
                                "location": {"selector": "[data-testid='job-location']"},
                                "salary": {"selector": "[data-testid='attribute_snippet_testid']"},
                                "description": {"selector": "[data-testid='job-snippet']"},
                                "posted_date": {"selector": "[data-testid='myJobsStateDate']"},
                                "job_url": {"selector": "h2 a", "attribute": "href"}
                            }
                        }
                    }
                }
                
                config = CrawlerRunConfig(
                    extraction_strategy=extraction_strategy,  # type: ignore
                    wait_for="css:[data-jk]",
                    delay_before_return_html=2
                )
                
                result = await self.crawler.arun(url=url, config=config)
                
                if result.success and result.extracted_content:
                    extracted = json.loads(result.extracted_content)
                    if 'job_cards' in extracted:
                        for job in extracted['job_cards']:
                            job_data = await self.process_indeed_job(job, keywords, location)
                            if job_data and not self.is_duplicate(job_data['url']):
                                jobs.append(job_data)
                                self.existing_jobs.add(job_data['url'])
                
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error scraping Indeed page {page + 1}: {str(e)}")
                continue
        
        return jobs
    
    async def scrape_careerbuilder_jobs(self, keywords: str, location: str = "", 
                                      pages: int = 5) -> List[Dict]:
        """Scrape job listings from CareerBuilder."""
        jobs = []
        
        if not self.crawler:
            logger.error("Crawler not initialized")
            return jobs
        
        for page in range(1, pages + 1):
            url = self.build_careerbuilder_search_url(keywords, location, page)
            
            logger.info(f"Scraping CareerBuilder page {page}: {url}")
            
            try:
                extraction_strategy = {
                    "type": "css_extractor", 
                    "params": {
                        "job_cards": {
                            "selector": "[data-cy='job-result-card']",
                            "fields": {
                                "title": {"selector": "[data-cy='job-title'] a"},
                                "company": {"selector": "[data-cy='job-company-name']"},
                                "location": {"selector": "[data-cy='job-location']"},
                                "salary": {"selector": "[data-cy='job-pay']"},
                                "description": {"selector": "[data-cy='job-snippet']"},
                                "posted_date": {"selector": "[data-cy='job-posted-date']"},
                                "job_url": {"selector": "[data-cy='job-title'] a", "attribute": "href"}
                            }
                        }
                    }
                }
                
                config = CrawlerRunConfig(
                    extraction_strategy=extraction_strategy,  # type: ignore
                    wait_for="css:[data-cy='job-result-card']",
                    delay_before_return_html=2
                )
                
                result = await self.crawler.arun(url=url, config=config)
                
                if result.success and result.extracted_content:
                    extracted = json.loads(result.extracted_content)
                    if 'job_cards' in extracted:
                        for job in extracted['job_cards']:
                            job_data = await self.process_careerbuilder_job(job, keywords, location)
                            if job_data and not self.is_duplicate(job_data['url']):
                                jobs.append(job_data)
                                self.existing_jobs.add(job_data['url'])
                
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error scraping CareerBuilder page {page}: {str(e)}")
                continue
        
        return jobs
    
    def is_duplicate(self, job_url: str) -> bool:
        """Check if job URL already exists in database."""
        return job_url in self.existing_jobs
    
    async def get_full_job_description(self, job_url: str) -> str:
        """Fetch full job description from job URL."""
        if not self.crawler:
            logger.error("Crawler not initialized")
            return ""
            
        try:
            config = CrawlerRunConfig(
                wait_for="body",
                delay_before_return_html=1
            )
            
            result = await self.crawler.arun(url=job_url, config=config)
            
            if result.success and result.cleaned_html:
                # Extract text content from HTML
                text = re.sub(r'<[^>]+>', ' ', result.cleaned_html)
                text = re.sub(r'\s+', ' ', text).strip()
                return text[:5000]  # Limit to 5000 characters
                
        except Exception as e:
            logger.error(f"Error fetching full job description: {e}")
        
        return ""
    
    async def process_indeed_job(self, job: Dict, keywords: str, location: str) -> Optional[Dict]:
        """Process and clean Indeed job data."""
        try:
            job_url = self.build_full_url(job.get('job_url', ''), 'indeed.com')
            
            # Get full job description
            full_description = await self.get_full_job_description(job_url)
            description_text = full_description or self.clean_text(job.get('description', ''))
            
            # Extract skills from job description
            skills = self.skill_extractor.extract_skills_from_text(description_text)
            
            # Parse location
            location_parts = self.parse_location(job.get('location', ''))
            
            job_data = {
                "id": str(uuid.uuid4()),
                "title": self.clean_text(job.get('title', '')),
                "company": self.clean_text(job.get('company', '')),
                "job_location": location_parts['city'],
                "job_state": location_parts['state'],
                "date": date.today(),
                "site": "Indeed",
                "job_description": description_text,
                "salary": self.clean_text(job.get('salary', '')) or "N/A",
                "url": job_url,
                "applied": False,
                "search_term": keywords,
                "skills": skills,
                "priority": 0,
                "status": "new",
                "category": None,
                "inserted_at": datetime.utcnow(),
                "last_verified": None,
                "user_id": None
            }
            
            if job_data['title'] and job_data['company']:
                return job_data
            
        except Exception as e:
            logger.error(f"Error processing Indeed job: {str(e)}")
        
        return None
    
    async def process_careerbuilder_job(self, job: Dict, keywords: str, location: str) -> Optional[Dict]:
        """Process and clean CareerBuilder job data."""
        try:
            job_url = self.build_full_url(job.get('job_url', ''), 'careerbuilder.com')
            
            # Get full job description
            full_description = await self.get_full_job_description(job_url)
            description_text = full_description or self.clean_text(job.get('description', ''))
            
            # Extract skills from job description
            skills = self.skill_extractor.extract_skills_from_text(description_text)
            
            # Parse location
            location_parts = self.parse_location(job.get('location', ''))
            
            job_data = {
                "id": str(uuid.uuid4()),
                "title": self.clean_text(job.get('title', '')),
                "company": self.clean_text(job.get('company', '')),
                "job_location": location_parts['city'],
                "job_state": location_parts['state'],
                "date": date.today(),
                "site": "CareerBuilder",
                "job_description": description_text,
                "salary": self.clean_text(job.get('salary', '')) or "N/A",
                "url": job_url,
                "applied": False,
                "search_term": keywords,
                "skills": skills,
                "priority": 0,
                "status": "new",
                "category": None,
                "inserted_at": datetime.utcnow(),
                "last_verified": None,
                "user_id": None
            }
            
            if job_data['title'] and job_data['company']:
                return job_data
                
        except Exception as e:
            logger.error(f"Error processing CareerBuilder job: {str(e)}")
        
        return None
    
    def parse_location(self, location_str: str) -> Dict[str, str]:
        """Parse location string into city and state."""
        if not location_str:
            return {"city": "", "state": ""}
        
        # Common patterns: "City, ST" or "City, State"
        parts = [part.strip() for part in location_str.split(',')]
        
        if len(parts) >= 2:
            city = parts[0]
            state = parts[1]
            # Handle state abbreviations
            if len(state) > 2:
                state = state[:2].upper()
            return {"city": city, "state": state}
        else:
            return {"city": location_str, "state": ""}
    
    def clean_text(self, text: Union[str, None]) -> str:
        """Clean and normalize text data."""
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'<[^>]+>', '', text)
        return text
    
    def build_full_url(self, url: str, base_domain: str) -> str:
        """Build full URL from relative URL."""
        if not url:
            return ""
        
        if url.startswith('http'):
            return url
        elif url.startswith('/'):
            return f"https://{base_domain}{url}"
        else:
            return f"https://{base_domain}/{url}"
    
    def save_to_csv(self, jobs: List[Dict]):
        """Save jobs to CSV file."""
        if not jobs:
            return
        
        try:
            fieldnames = [
                'id', 'title', 'company', 'job_location', 'job_state', 'date',
                'site', 'salary', 'url', 'search_term', 'skills', 'priority',
                'status', 'category', 'inserted_at'
            ]
            
            with open(self.csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for job in jobs:
                    # Convert lists and dates to strings for CSV
                    csv_job = job.copy()
                    csv_job['skills'] = ','.join(job.get('skills', []))
                    csv_job['date'] = str(job.get('date', ''))
                    csv_job['inserted_at'] = str(job.get('inserted_at', ''))
                    
                    writer.writerow(csv_job)
            
            logger.info(f"Saved {len(jobs)} jobs to CSV: {self.csv_filename}")
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    async def save_jobs_to_supabase(self, jobs: List[Dict], table_name: str = 'jobs') -> bool:
        """Save job listings to Supabase."""
        if not jobs:
            logger.info("No jobs to save")
            return True
            
        try:
            batch_size = 50
            
            for i in range(0, len(jobs), batch_size):
                batch = jobs[i:i + batch_size]
                
                # Convert dates to ISO format for Supabase
                for job in batch:
                    if isinstance(job.get('date'), date):
                        job['date'] = job['date'].isoformat()
                    if isinstance(job.get('inserted_at'), datetime):
                        job['inserted_at'] = job['inserted_at'].isoformat()
                
                result = self.supabase.table(table_name).insert(batch).execute()
                logger.info(f"Saved batch {i//batch_size + 1}: {len(batch)} jobs")
            
            logger.info(f"Successfully saved {len(jobs)} jobs to Supabase")
            return True
            
        except Exception as e:
            logger.error(f"Error saving jobs to Supabase: {str(e)}")
            return False
    
    async def scrape_and_save(self, keywords: str, location: str = "", 
                            pages: int = 5, table_name: str = 'jobs') -> Dict:
        """Complete scraping workflow."""
        results = {
            'indeed_jobs': 0,
            'careerbuilder_jobs': 0,
            'total_jobs': 0,
            'duplicates_skipped': 0,
            'csv_file': self.csv_filename,
            'success': False
        }
        
        try:
            logger.info(f"Starting job scrape for: {keywords} in {location}")
            
            # Scrape Indeed
            indeed_jobs = await self.scrape_indeed_jobs(keywords, location, pages)
            results['indeed_jobs'] = len(indeed_jobs)
            
            # Scrape CareerBuilder
            careerbuilder_jobs = await self.scrape_careerbuilder_jobs(keywords, location, pages)
            results['careerbuilder_jobs'] = len(careerbuilder_jobs)
            
            # Combine all jobs
            all_jobs = indeed_jobs + careerbuilder_jobs
            results['total_jobs'] = len(all_jobs)
            
            # Count duplicates
            initial_count = len(self.existing_jobs)
            final_count = len(self.existing_jobs)
            results['duplicates_skipped'] = final_count - initial_count
            
            # Save to CSV
            self.save_to_csv(all_jobs)
            
            # Save to Supabase
            if all_jobs:
                save_success = await self.save_jobs_to_supabase(all_jobs, table_name)
                results['success'] = save_success
            else:
                logger.warning("No jobs found to save")
                results['success'] = True
            
            logger.info(f"Scraping complete: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error in scrape_and_save: {str(e)}")
            results['error'] = str(e)
            return results


class ResumeSkillMatcher:
    """Service to match resume skills with job listings."""
    
    def __init__(self, supabase_url: str, supabase_key: str, skills_file_path: str = "utils/skills.json"):
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.skill_extractor = SkillExtractor(skills_file_path)
    
    def extract_skills_from_resume(self, resume_text: str) -> List[str]:
        """Extract skills from resume text."""
        return self.skill_extractor.extract_skills_from_text(resume_text)
    
    def calculate_skill_match_score(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Calculate skill match score between resume and job."""
        if not job_skills:
            return 0.0
        
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        matching_skills = set(resume_skills_lower) & set(job_skills_lower)
        return len(matching_skills) / len(job_skills_lower)
    
    async def get_recommended_jobs(self, resume_text: str, min_score: float = 0.2, 
                                 limit: int = 50, user_id: Optional[str] = None) -> List[Dict]:
        """Get recommended jobs based on resume skills."""
        try:
            # Extract skills from resume
            resume_skills = self.extract_skills_from_resume(resume_text)
            
            if not resume_skills:
                logger.warning("No skills found in resume")
                return []
            
            # Get all jobs from database
            query = self.supabase.table('jobs').select('*')
            if user_id:
                query = query.eq('user_id', user_id)
            
            result = query.execute()
            jobs = result.data
            
            # Calculate match scores
            job_matches = []
            for job in jobs:
                job_skills = job.get('skills', [])
                if isinstance(job_skills, str):
                    job_skills = job_skills.split(',') if job_skills else []
                
                score = self.calculate_skill_match_score(resume_skills, job_skills)
                
                if score >= min_score:
                    job['match_score'] = score
                    job['matching_skills'] = list(set(resume_skills) & set(job_skills))
                    job_matches.append(job)
            
            # Sort by match score (highest first)
            job_matches.sort(key=lambda x: x['match_score'], reverse=True)
            
            return job_matches[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recommended jobs: {e}")
            return []


# Example usage
async def main():
    """Example usage of the JobScraper and ResumeSkillMatcher"""
    
    # Your Supabase credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
    # Scraping
    async with JobScraper(SUPABASE_URL, SUPABASE_KEY) as scraper:
        results = await scraper.scrape_and_save(
            keywords="python developer",
            location="New York, NY",
            pages=3
        )
        print(f"Scraping Results: {results}")
    
    # Resume matching example
    matcher = ResumeSkillMatcher(SUPABASE_URL, SUPABASE_KEY)
    
    sample_resume = """
    Experienced Python developer with 5 years of experience in Django, Flask, 
    and React. Proficient in SQL, PostgreSQL, and AWS cloud services.
    """
    
    recommended_jobs = await matcher.get_recommended_jobs(
        resume_text=sample_resume,
        min_score=0.3,
        limit=10
    )
    
    print(f"Found {len(recommended_jobs)} recommended jobs")
    for job in recommended_jobs[:3]:  # Show top 3
        print(f"- {job['title']} at {job['company']} (Score: {job['match_score']:.2f})")

if __name__ == "__main__":
    asyncio.run(main())

# import asyncio
# import json
# import re
# import csv
# import uuid
# from datetime import datetime, date
# from typing import List, Dict, Optional, Set
# from urllib.parse import urlencode, urlparse
# import os
# from pathlib import Path
# from supabase import create_client
# import os
# from dotenv import load_dotenv

# from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
# from supabase import create_client, Client
# import logging
# load_dotenv()
# url = os.getenv("SUPABASE_URL")
# key = os.getenv("SUPABASE_ANON_KEY")
# if not url or not key:
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

# supabase = create_client(url, key)
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class SkillExtractor:
#     def __init__(self, skills_file_path: str = "utils/skills.json"):
#         """
#         Initialize skill extractor with skills from file.
        
#         Args:
#             skills_file_path: Path to skills JSON file
#         """
#         self.skills = self.load_skills(skills_file_path)
#         self.skills_lower = [skill.lower() for skill in self.skills]
        
#     def load_skills(self, file_path: str) -> List[str]:
#         """Load skills from JSON file."""
#         try:
#             if os.path.exists(file_path):
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     data = json.load(f)
#                     # Handle different JSON structures
#                     if isinstance(data, list):
#                         return data
#                     elif isinstance(data, dict):
#                         return data.get('skills', [])
#             else:
#                 logger.warning(f"Skills file not found: {file_path}")
#                 return self.get_default_skills()
#         except Exception as e:
#             logger.error(f"Error loading skills file: {e}")
#             return self.get_default_skills()
    
#     def get_default_skills(self) -> List[str]:
#         """Return default skills list if file not found."""
#         return [
#             "Python", "JavaScript", "Java", "C++", "C#", "HTML", "CSS", "React", 
#             "Node.js", "Django", "Flask", "Spring", "Angular", "Vue.js", "SQL", 
#             "MongoDB", "PostgreSQL", "MySQL", "Git", "Docker", "Kubernetes", 
#             "AWS", "Azure", "GCP", "Linux", "Windows", "MacOS", "Agile", "Scrum",
#             "Machine Learning", "AI", "Data Science", "Pandas", "NumPy", "TensorFlow",
#             "PyTorch", "REST API", "GraphQL", "Microservices", "CI/CD", "Jenkins",
#             "Terraform", "Ansible", "Redis", "Elasticsearch", "Kafka", "RabbitMQ"
#         ]
    
#     def extract_skills_from_text(self, text: str) -> List[str]:
#         """Extract skills from job description text."""
#         if not text:
#             return []
        
#         text_lower = text.lower()
#         found_skills = []
        
#         for skill in self.skills:
#             skill_lower = skill.lower()
            
#             # Use word boundaries to avoid partial matches
#             pattern = r'\b' + re.escape(skill_lower) + r'\b'
            
#             if re.search(pattern, text_lower):
#                 found_skills.append(skill)
        
#         return list(set(found_skills))  # Remove duplicates


# class JobScraper:
#     def __init__(self, supabase_url: str, supabase_key: str, skills_file_path: str = "utils/skills.json"):
#         """
#         Initialize the job scraper with Supabase credentials and skill extractor.
        
#         Args:
#             supabase_url: Your Supabase project URL
#             supabase_key: Your Supabase anon/service key
#             skills_file_path: Path to skills JSON file
#         """
#         self.supabase: Client = create_client(supabase_url, supabase_key)
#         self.crawler = None
#         self.skill_extractor = SkillExtractor(skills_file_path)
#         self.existing_jobs: Set[str] = set()
#         self.csv_filename = f"scraped_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
#     async def __aenter__(self):
#         """Async context manager entry"""
#         self.crawler = AsyncWebCrawler(verbose=True)
#         await self.crawler.__aenter__()
#         await self.load_existing_jobs()
#         return self
        
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         """Async context manager exit"""
#         if self.crawler:
#             await self.crawler.__aexit__(exc_type, exc_val, exc_tb)
    
#     async def load_existing_jobs(self):
#         """Load existing job URLs from database to prevent duplicates."""
#         try:
#             result = self.supabase.table('jobs').select('url').execute()
#             self.existing_jobs = {job['url'] for job in result.data if job.get('url')}
#             logger.info(f"Loaded {len(self.existing_jobs)} existing job URLs for duplicate detection")
#         except Exception as e:
#             logger.error(f"Error loading existing jobs: {e}")
#             self.existing_jobs = set()
    
#     def build_indeed_search_url(self, keywords: str, location: str = "", 
#                                start: int = 0, limit: int = 50) -> str:
#         """Build Indeed search URL with parameters."""
#         base_url = "https://www.indeed.com/jobs"
#         params = {
#             'q': keywords,
#             'l': location,
#             'start': start,
#             'limit': limit
#         }
#         return f"{base_url}?{urlencode(params)}"
    
#     def build_careerbuilder_search_url(self, keywords: str, location: str = "", 
#                                      page: int = 1) -> str:
#         """Build CareerBuilder search URL with parameters."""
#         base_url = "https://www.careerbuilder.com/jobs"
#         params = {
#             'keywords': keywords,
#             'location': location,
#             'page_number': page
#         }
#         return f"{base_url}?{urlencode(params)}"
    
#     async def scrape_indeed_jobs(self, keywords: str, location: str = "", 
#                                pages: int = 5) -> List[Dict]:
#         """Scrape job listings from Indeed."""
#         jobs = []
        
#         for page in range(pages):
#             start = page * 10
#             url = self.build_indeed_search_url(keywords, location, start)
            
#             logger.info(f"Scraping Indeed page {page + 1}: {url}")
            
#             try:
#                 extraction_strategy = {
#                     "type": "css_extractor",
#                     "params": {
#                         "job_cards": {
#                             "selector": "[data-jk]",
#                             "fields": {
#                                 "job_id": {"selector": "[data-jk]", "attribute": "data-jk"},
#                                 "title": {"selector": "h2 a span", "attribute": "title"},
#                                 "company": {"selector": "[data-testid='company-name']"},
#                                 "location": {"selector": "[data-testid='job-location']"},
#                                 "salary": {"selector": "[data-testid='attribute_snippet_testid']"},
#                                 "description": {"selector": "[data-testid='job-snippet']"},
#                                 "posted_date": {"selector": "[data-testid='myJobsStateDate']"},
#                                 "job_url": {"selector": "h2 a", "attribute": "href"}
#                             }
#                         }
#                     }
#                 }
                
#                 config = CrawlerRunConfig(
#                     extraction_strategy=extraction_strategy,
#                     wait_for="css:[data-jk]",
#                     delay_before_return_html=2
#                 )
                
#                 result = await self.crawler.arun(url=url, config=config)
                
#                 if result.success and result.extracted_content:
#                     extracted = json.loads(result.extracted_content)
#                     if 'job_cards' in extracted:
#                         for job in extracted['job_cards']:
#                             job_data = await self.process_indeed_job(job, keywords, location)
#                             if job_data and not self.is_duplicate(job_data['url']):
#                                 jobs.append(job_data)
#                                 self.existing_jobs.add(job_data['url'])
                
#                 await asyncio.sleep(2)
                
#             except Exception as e:
#                 logger.error(f"Error scraping Indeed page {page + 1}: {str(e)}")
#                 continue
        
#         return jobs
    
#     async def scrape_careerbuilder_jobs(self, keywords: str, location: str = "", 
#                                       pages: int = 5) -> List[Dict]:
#         """Scrape job listings from CareerBuilder."""
#         jobs = []
        
#         for page in range(1, pages + 1):
#             url = self.build_careerbuilder_search_url(keywords, location, page)
            
#             logger.info(f"Scraping CareerBuilder page {page}: {url}")
            
#             try:
#                 extraction_strategy = {
#                     "type": "css_extractor", 
#                     "params": {
#                         "job_cards": {
#                             "selector": "[data-cy='job-result-card']",
#                             "fields": {
#                                 "title": {"selector": "[data-cy='job-title'] a"},
#                                 "company": {"selector": "[data-cy='job-company-name']"},
#                                 "location": {"selector": "[data-cy='job-location']"},
#                                 "salary": {"selector": "[data-cy='job-pay']"},
#                                 "description": {"selector": "[data-cy='job-snippet']"},
#                                 "posted_date": {"selector": "[data-cy='job-posted-date']"},
#                                 "job_url": {"selector": "[data-cy='job-title'] a", "attribute": "href"}
#                             }
#                         }
#                     }
#                 }
                
#                 config = CrawlerRunConfig(
#                     extraction_strategy=extraction_strategy,
#                     wait_for="css:[data-cy='job-result-card']",
#                     delay_before_return_html=2
#                 )
                
#                 result = await self.crawler.arun(url=url, config=config)
                
#                 if result.success and result.extracted_content:
#                     extracted = json.loads(result.extracted_content)
#                     if 'job_cards' in extracted:
#                         for job in extracted['job_cards']:
#                             job_data = await self.process_careerbuilder_job(job, keywords, location)
#                             if job_data and not self.is_duplicate(job_data['url']):
#                                 jobs.append(job_data)
#                                 self.existing_jobs.add(job_data['url'])
                
#                 await asyncio.sleep(2)
                
#             except Exception as e:
#                 logger.error(f"Error scraping CareerBuilder page {page}: {str(e)}")
#                 continue
        
#         return jobs
    
#     def is_duplicate(self, job_url: str) -> bool:
#         """Check if job URL already exists in database."""
#         return job_url in self.existing_jobs
    
#     async def get_full_job_description(self, job_url: str) -> str:
#         """Fetch full job description from job URL."""
#         try:
#             config = CrawlerRunConfig(
#                 wait_for="body",
#                 delay_before_return_html=1
#             )
            
#             result = await self.crawler.arun(url=job_url, config=config)
            
#             if result.success and result.cleaned_html:
#                 # Extract text content from HTML
#                 text = re.sub(r'<[^>]+>', ' ', result.cleaned_html)
#                 text = re.sub(r'\s+', ' ', text).strip()
#                 return text[:5000]  # Limit to 5000 characters
                
#         except Exception as e:
#             logger.error(f"Error fetching full job description: {e}")
        
#         return ""
    
#     async def process_indeed_job(self, job: Dict, keywords: str, location: str) -> Optional[Dict]:
#         """Process and clean Indeed job data."""
#         try:
#             job_url = self.build_full_url(job.get('job_url', ''), 'indeed.com')
            
#             # Get full job description
#             full_description = await self.get_full_job_description(job_url)
#             description_text = full_description or self.clean_text(job.get('description', ''))
            
#             # Extract skills from job description
#             skills = self.skill_extractor.extract_skills_from_text(description_text)
            
#             # Parse location
#             location_parts = self.parse_location(job.get('location', ''))
            
#             job_data = {
#                 "id": str(uuid.uuid4()),
#                 "title": self.clean_text(job.get('title', '')),
#                 "company": self.clean_text(job.get('company', '')),
#                 "job_location": location_parts['city'],
#                 "job_state": location_parts['state'],
#                 "date": date.today(),
#                 "site": "Indeed",
#                 "job_description": description_text,
#                 "salary": self.clean_text(job.get('salary', '')) or "N/A",
#                 "url": job_url,
#                 "applied": False,
#                 "search_term": keywords,
#                 "skills": skills,
#                 "priority": 0,
#                 "status": "new",
#                 "category": None,
#                 "inserted_at": datetime.utcnow(),
#                 "last_verified": None,
#                 "user_id": None
#             }
            
#             if job_data['title'] and job_data['company']:
#                 return job_data
            
#         except Exception as e:
#             logger.error(f"Error processing Indeed job: {str(e)}")
        
#         return None
    
#     async def process_careerbuilder_job(self, job: Dict, keywords: str, location: str) -> Optional[Dict]:
#         """Process and clean CareerBuilder job data."""
#         try:
#             job_url = self.build_full_url(job.get('job_url', ''), 'careerbuilder.com')
            
#             # Get full job description
#             full_description = await self.get_full_job_description(job_url)
#             description_text = full_description or self.clean_text(job.get('description', ''))
            
#             # Extract skills from job description
#             skills = self.skill_extractor.extract_skills_from_text(description_text)
            
#             # Parse location
#             location_parts = self.parse_location(job.get('location', ''))
            
#             job_data = {
#                 "id": str(uuid.uuid4()),
#                 "title": self.clean_text(job.get('title', '')),
#                 "company": self.clean_text(job.get('company', '')),
#                 "job_location": location_parts['city'],
#                 "job_state": location_parts['state'],
#                 "date": date.today(),
#                 "site": "CareerBuilder",
#                 "job_description": description_text,
#                 "salary": self.clean_text(job.get('salary', '')) or "N/A",
#                 "url": job_url,
#                 "applied": False,
#                 "search_term": keywords,
#                 "skills": skills,
#                 "priority": 0,
#                 "status": "new",
#                 "category": None,
#                 "inserted_at": datetime.utcnow(),
#                 "last_verified": None,
#                 "user_id": None
#             }
            
#             if job_data['title'] and job_data['company']:
#                 return job_data
                
#         except Exception as e:
#             logger.error(f"Error processing CareerBuilder job: {str(e)}")
        
#         return None
    
#     def parse_location(self, location_str: str) -> Dict[str, str]:
#         """Parse location string into city and state."""
#         if not location_str:
#             return {"city": "", "state": ""}
        
#         # Common patterns: "City, ST" or "City, State"
#         parts = [part.strip() for part in location_str.split(',')]
        
#         if len(parts) >= 2:
#             city = parts[0]
#             state = parts[1]
#             # Handle state abbreviations
#             if len(state) > 2:
#                 state = state[:2].upper()
#             return {"city": city, "state": state}
#         else:
#             return {"city": location_str, "state": ""}
    
#     def clean_text(self, text: str) -> str:
#         """Clean and normalize text data."""
#         if not text:
#             return ""
        
#         text = re.sub(r'\s+', ' ', text.strip())
#         text = re.sub(r'<[^>]+>', '', text)
#         return text
    
#     def build_full_url(self, url: str, base_domain: str) -> str:
#         """Build full URL from relative URL."""
#         if not url:
#             return ""
        
#         if url.startswith('http'):
#             return url
#         elif url.startswith('/'):
#             return f"https://{base_domain}{url}"
#         else:
#             return f"https://{base_domain}/{url}"
    
#     def save_to_csv(self, jobs: List[Dict]):
#         """Save jobs to CSV file."""
#         if not jobs:
#             return
        
#         try:
#             fieldnames = [
#                 'id', 'title', 'company', 'job_location', 'job_state', 'date',
#                 'site', 'salary', 'url', 'search_term', 'skills', 'priority',
#                 'status', 'category', 'inserted_at'
#             ]
            
#             with open(self.csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
                
#                 for job in jobs:
#                     # Convert lists and dates to strings for CSV
#                     csv_job = job.copy()
#                     csv_job['skills'] = ','.join(job.get('skills', []))
#                     csv_job['date'] = str(job.get('date', ''))
#                     csv_job['inserted_at'] = str(job.get('inserted_at', ''))
                    
#                     writer.writerow(csv_job)
            
#             logger.info(f"Saved {len(jobs)} jobs to CSV: {self.csv_filename}")
            
#         except Exception as e:
#             logger.error(f"Error saving to CSV: {e}")
    
#     async def save_jobs_to_supabase(self, jobs: List[Dict], table_name: str = 'jobs') -> bool:
#         """Save job listings to Supabase."""
#         if not jobs:
#             logger.info("No jobs to save")
#             return True
            
#         try:
#             batch_size = 50
            
#             for i in range(0, len(jobs), batch_size):
#                 batch = jobs[i:i + batch_size]
                
#                 # Convert dates to ISO format for Supabase
#                 for job in batch:
#                     if isinstance(job.get('date'), date):
#                         job['date'] = job['date'].isoformat()
#                     if isinstance(job.get('inserted_at'), datetime):
#                         job['inserted_at'] = job['inserted_at'].isoformat()
                
#                 result = self.supabase.table(table_name).insert(batch).execute()
#                 logger.info(f"Saved batch {i//batch_size + 1}: {len(batch)} jobs")
            
#             logger.info(f"Successfully saved {len(jobs)} jobs to Supabase")
#             return True
            
#         except Exception as e:
#             logger.error(f"Error saving jobs to Supabase: {str(e)}")
#             return False
    
#     async def scrape_and_save(self, keywords: str, location: str = "", 
#                             pages: int = 5, table_name: str = 'jobs') -> Dict:
#         """Complete scraping workflow."""
#         results = {
#             'indeed_jobs': 0,
#             'careerbuilder_jobs': 0,
#             'total_jobs': 0,
#             'duplicates_skipped': 0,
#             'csv_file': self.csv_filename,
#             'success': False
#         }
        
#         try:
#             logger.info(f"Starting job scrape for: {keywords} in {location}")
            
#             # Scrape Indeed
#             indeed_jobs = await self.scrape_indeed_jobs(keywords, location, pages)
#             results['indeed_jobs'] = len(indeed_jobs)
            
#             # Scrape CareerBuilder
#             careerbuilder_jobs = await self.scrape_careerbuilder_jobs(keywords, location, pages)
#             results['careerbuilder_jobs'] = len(careerbuilder_jobs)
            
#             # Combine all jobs
#             all_jobs = indeed_jobs + careerbuilder_jobs
#             results['total_jobs'] = len(all_jobs)
            
#             # Count duplicates
#             initial_count = len(self.existing_jobs)
#             final_count = len(self.existing_jobs)
#             results['duplicates_skipped'] = final_count - initial_count
            
#             # Save to CSV
#             self.save_to_csv(all_jobs)
            
#             # Save to Supabase
#             if all_jobs:
#                 save_success = await self.save_jobs_to_supabase(all_jobs, table_name)
#                 results['success'] = save_success
#             else:
#                 logger.warning("No jobs found to save")
#                 results['success'] = True
            
#             logger.info(f"Scraping complete: {results}")
#             return results
            
#         except Exception as e:
#             logger.error(f"Error in scrape_and_save: {str(e)}")
#             results['error'] = str(e)
#             return results


# class ResumeSkillMatcher:
#     """Service to match resume skills with job listings."""
    
#     def __init__(self, supabase_url: str, supabase_key: str, skills_file_path: str = "utils/skills.json"):
#         self.supabase: Client = create_client(supabase_url, supabase_key)
#         self.skill_extractor = SkillExtractor(skills_file_path)
    
#     def extract_skills_from_resume(self, resume_text: str) -> List[str]:
#         """Extract skills from resume text."""
#         return self.skill_extractor.extract_skills_from_text(resume_text)
    
#     def calculate_skill_match_score(self, resume_skills: List[str], job_skills: List[str]) -> float:
#         """Calculate skill match score between resume and job."""
#         if not job_skills:
#             return 0.0
        
#         resume_skills_lower = [skill.lower() for skill in resume_skills]
#         job_skills_lower = [skill.lower() for skill in job_skills]
        
#         matching_skills = set(resume_skills_lower) & set(job_skills_lower)
#         return len(matching_skills) / len(job_skills_lower)
    
#     async def get_recommended_jobs(self, resume_text: str, min_score: float = 0.2, 
#                                  limit: int = 50, user_id: str = None) -> List[Dict]:
#         """Get recommended jobs based on resume skills."""
#         try:
#             # Extract skills from resume
#             resume_skills = self.extract_skills_from_resume(resume_text)
            
#             if not resume_skills:
#                 logger.warning("No skills found in resume")
#                 return []
            
#             # Get all jobs from database
#             query = self.supabase.table('jobs').select('*')
#             if user_id:
#                 query = query.eq('user_id', user_id)
            
#             result = query.execute()
#             jobs = result.data
            
#             # Calculate match scores
#             job_matches = []
#             for job in jobs:
#                 job_skills = job.get('skills', [])
#                 if isinstance(job_skills, str):
#                     job_skills = job_skills.split(',') if job_skills else []
                
#                 score = self.calculate_skill_match_score(resume_skills, job_skills)
                
#                 if score >= min_score:
#                     job['match_score'] = score
#                     job['matching_skills'] = list(set(resume_skills) & set(job_skills))
#                     job_matches.append(job)
            
#             # Sort by match score (highest first)
#             job_matches.sort(key=lambda x: x['match_score'], reverse=True)
            
#             return job_matches[:limit]
            
#         except Exception as e:
#             logger.error(f"Error getting recommended jobs: {e}")
#             return []


# # Example usage
# async def main():
#     """Example usage of the JobScraper and ResumeSkillMatcher"""
    
#     # Your Supabase credentials
#     SUPABASE_URL = "your-supabase-url"
#     SUPABASE_KEY = "your-supabase-anon-key"
    
#     # Scraping
#     async with JobScraper(SUPABASE_URL, SUPABASE_KEY) as scraper:
#         results = await scraper.scrape_and_save(
#             keywords="python developer",
#             location="New York, NY",
#             pages=3
#         )
#         print(f"Scraping Results: {results}")
    
#     # Resume matching example
#     matcher = ResumeSkillMatcher(SUPABASE_URL, SUPABASE_KEY)
    
#     sample_resume = """
#     Experienced Python developer with 5 years of experience in Django, Flask, 
#     and React. Proficient in SQL, PostgreSQL, and AWS cloud services.
#     """
    
#     recommended_jobs = await matcher.get_recommended_jobs(
#         resume_text=sample_resume,
#         min_score=0.3,
#         limit=10
#     )
    
#     print(f"Found {len(recommended_jobs)} recommended jobs")
#     for job in recommended_jobs[:3]:  # Show top 3
#         print(f"- {job['title']} at {job['company']} (Score: {job['match_score']:.2f})")


# if __name__ == "__main__":
#     asyncio.run(main())











# import asyncio
# import json
# import re
# from datetime import datetime
# from typing import List, Dict, Optional
# from urllib.parse import urlencode, urlparse

# from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
# from supabase import create_client, Client
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class JobScraper:
#     def __init__(self, supabase_url: str, supabase_key: str):
#         """
#         Initialize the job scraper with Supabase credentials.
        
#         Args:
#             supabase_url: Your Supabase project URL
#             supabase_key: Your Supabase anon/service key
#         """
#         self.supabase: Client = create_client(supabase_url, supabase_key)
#         self.crawler = None
        
#     async def __aenter__(self):
#         """Async context manager entry"""
#         self.crawler = AsyncWebCrawler(verbose=True)
#         await self.crawler.__aenter__()
#         return self
        
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         """Async context manager exit"""
#         if self.crawler:
#             await self.crawler.__aexit__(exc_type, exc_val, exc_tb)
    
#     def build_indeed_search_url(self, keywords: str, location: str = "", 
#                                start: int = 0, limit: int = 50) -> str:
#         """
#         Build Indeed search URL with parameters.
        
#         Args:
#             keywords: Job search keywords
#             location: Job location
#             start: Starting position for pagination
#             limit: Number of results per page
#         """
#         base_url = "https://www.indeed.com/jobs"
#         params = {
#             'q': keywords,
#             'l': location,
#             'start': start,
#             'limit': limit
#         }
#         return f"{base_url}?{urlencode(params)}"
    
#     def build_careerbuilder_search_url(self, keywords: str, location: str = "", 
#                                      page: int = 1) -> str:
#         """
#         Build CareerBuilder search URL with parameters.
        
#         Args:
#             keywords: Job search keywords
#             location: Job location
#             page: Page number for pagination
#         """
#         base_url = "https://www.careerbuilder.com/jobs"
#         params = {
#             'keywords': keywords,
#             'location': location,
#             'page_number': page
#         }
#         return f"{base_url}?{urlencode(params)}"
    
#     async def scrape_indeed_jobs(self, keywords: str, location: str = "", 
#                                pages: int = 5) -> List[Dict]:
#         """
#         Scrape job listings from Indeed.
        
#         Args:
#             keywords: Job search keywords
#             location: Job location
#             pages: Number of pages to scrape
#         """
#         jobs = []
        
#         for page in range(pages):
#             start = page * 10  # Indeed shows 10 jobs per page
#             url = self.build_indeed_search_url(keywords, location, start)
            
#             logger.info(f"Scraping Indeed page {page + 1}: {url}")
            
#             try:
#                 # Custom extraction strategy for Indeed job listings
#                 extraction_strategy = {
#                     "type": "css_extractor",
#                     "params": {
#                         "job_cards": {
#                             "selector": "[data-jk]",
#                             "fields": {
#                                 "job_id": {"selector": "[data-jk]", "attribute": "data-jk"},
#                                 "title": {"selector": "h2 a span", "attribute": "title"},
#                                 "company": {"selector": "[data-testid='company-name']"},
#                                 "location": {"selector": "[data-testid='job-location']"},
#                                 "salary": {"selector": "[data-testid='attribute_snippet_testid']"},
#                                 "description": {"selector": "[data-testid='job-snippet']"},
#                                 "posted_date": {"selector": "[data-testid='myJobsStateDate']"},
#                                 "job_url": {"selector": "h2 a", "attribute": "href"}
#                             }
#                         }
#                     }
#                 }
                
#                 config = CrawlerRunConfig(
#                     extraction_strategy=extraction_strategy,
#                     wait_for="css:[data-jk]",
#                     delay_before_return_html=2
#                 )
                
#                 result = await self.crawler.arun(url=url, config=config)
                
#                 if result.success and result.extracted_content:
#                     extracted = json.loads(result.extracted_content)
#                     if 'job_cards' in extracted:
#                         for job in extracted['job_cards']:
#                             job_data = self.process_indeed_job(job, keywords, location)
#                             if job_data:
#                                 jobs.append(job_data)
                
#                 # Add delay between requests to be respectful
#                 await asyncio.sleep(2)
                
#             except Exception as e:
#                 logger.error(f"Error scraping Indeed page {page + 1}: {str(e)}")
#                 continue
        
#         return jobs
    
#     async def scrape_careerbuilder_jobs(self, keywords: str, location: str = "", 
#                                       pages: int = 5) -> List[Dict]:
#         """
#         Scrape job listings from CareerBuilder.
        
#         Args:
#             keywords: Job search keywords  
#             location: Job location
#             pages: Number of pages to scrape
#         """
#         jobs = []
        
#         for page in range(1, pages + 1):
#             url = self.build_careerbuilder_search_url(keywords, location, page)
            
#             logger.info(f"Scraping CareerBuilder page {page}: {url}")
            
#             try:
#                 # Custom extraction strategy for CareerBuilder job listings
#                 extraction_strategy = {
#                     "type": "css_extractor", 
#                     "params": {
#                         "job_cards": {
#                             "selector": "[data-cy='job-result-card']",
#                             "fields": {
#                                 "title": {"selector": "[data-cy='job-title'] a"},
#                                 "company": {"selector": "[data-cy='job-company-name']"},
#                                 "location": {"selector": "[data-cy='job-location']"},
#                                 "salary": {"selector": "[data-cy='job-pay']"},
#                                 "description": {"selector": "[data-cy='job-snippet']"},
#                                 "posted_date": {"selector": "[data-cy='job-posted-date']"},
#                                 "job_url": {"selector": "[data-cy='job-title'] a", "attribute": "href"}
#                             }
#                         }
#                     }
#                 }
                
#                 config = CrawlerRunConfig(
#                     extraction_strategy=extraction_strategy,
#                     wait_for="css:[data-cy='job-result-card']",
#                     delay_before_return_html=2
#                 )
                
#                 result = await self.crawler.arun(url=url, config=config)
                
#                 if result.success and result.extracted_content:
#                     extracted = json.loads(result.extracted_content)
#                     if 'job_cards' in extracted:
#                         for job in extracted['job_cards']:
#                             job_data = self.process_careerbuilder_job(job, keywords, location)
#                             if job_data:
#                                 jobs.append(job_data)
                
#                 # Add delay between requests
#                 await asyncio.sleep(2)
                
#             except Exception as e:
#                 logger.error(f"Error scraping CareerBuilder page {page}: {str(e)}")
#                 continue
        
#         return jobs
    
#     def process_indeed_job(self, job: Dict, keywords: str, location: str) -> Optional[Dict]:
#         """Process and clean Indeed job data."""
#         try:
#             # Clean and format job data
#             job_data = {
#                 'source': 'indeed',
#                 'job_id': job.get('job_id', ''),
#                 'title': self.clean_text(job.get('title', '')),
#                 'company': self.clean_text(job.get('company', '')),
#                 'location': self.clean_text(job.get('location', '')),
#                 'salary': self.clean_text(job.get('salary', '')),
#                 'description': self.clean_text(job.get('description', '')),
#                 'posted_date': self.parse_date(job.get('posted_date', '')),
#                 'job_url': self.build_full_url(job.get('job_url', ''), 'indeed.com'),
#                 'search_keywords': keywords,
#                 'search_location': location,
#                 'scraped_at': datetime.utcnow().isoformat()
#             }
            
#             # Only return if we have essential data
#             if job_data['title'] and job_data['company']:
#                 return job_data
            
#         except Exception as e:
#             logger.error(f"Error processing Indeed job: {str(e)}")
        
#         return None
    
#     def process_careerbuilder_job(self, job: Dict, keywords: str, location: str) -> Optional[Dict]:
#         """Process and clean CareerBuilder job data."""
#         try:
#             job_data = {
#                 'source': 'careerbuilder',
#                 'job_id': self.generate_job_id(job.get('job_url', '')),
#                 'title': self.clean_text(job.get('title', '')),
#                 'company': self.clean_text(job.get('company', '')),
#                 'location': self.clean_text(job.get('location', '')),
#                 'salary': self.clean_text(job.get('salary', '')),
#                 'description': self.clean_text(job.get('description', '')),
#                 'posted_date': self.parse_date(job.get('posted_date', '')),
#                 'job_url': self.build_full_url(job.get('job_url', ''), 'careerbuilder.com'),
#                 'search_keywords': keywords,
#                 'search_location': location,
#                 'scraped_at': datetime.utcnow().isoformat()
#             }
            
#             if job_data['title'] and job_data['company']:
#                 return job_data
                
#         except Exception as e:
#             logger.error(f"Error processing CareerBuilder job: {str(e)}")
        
#         return None
    
#     def clean_text(self, text: str) -> str:
#         """Clean and normalize text data."""
#         if not text:
#             return ""
        
#         # Remove extra whitespace and newlines
#         text = re.sub(r'\s+', ' ', text.strip())
        
#         # Remove any HTML tags that might have slipped through
#         text = re.sub(r'<[^>]+>', '', text)
        
#         return text
    
#     def parse_date(self, date_str: str) -> Optional[str]:
#         """Parse various date formats to ISO format."""
#         if not date_str:
#             return None
            
#         # Common patterns for job posting dates
#         patterns = [
#             r'(\d+)\s+days?\s+ago',
#             r'(\d+)\s+hours?\s+ago',
#             r'Posted\s+(\d+)\s+days?\s+ago',
#             r'Just posted',
#             r'Today'
#         ]
        
#         date_str = date_str.lower().strip()
        
#         if 'today' in date_str or 'just posted' in date_str:
#             return datetime.utcnow().isoformat()
        
#         for pattern in patterns:
#             match = re.search(pattern, date_str)
#             if match:
#                 try:
#                     days_ago = int(match.group(1)) if match.group(1).isdigit() else 0
#                     if 'hour' in date_str:
#                         days_ago = 0  # Same day
                    
#                     from datetime import timedelta
#                     post_date = datetime.utcnow() - timedelta(days=days_ago)
#                     return post_date.isoformat()
#                 except:
#                     continue
        
#         return None
    
#     def build_full_url(self, url: str, base_domain: str) -> str:
#         """Build full URL from relative URL."""
#         if not url:
#             return ""
        
#         if url.startswith('http'):
#             return url
#         elif url.startswith('/'):
#             return f"https://{base_domain}{url}"
#         else:
#             return f"https://{base_domain}/{url}"
    
#     def generate_job_id(self, url: str) -> str:
#         """Generate a job ID from URL or other data."""
#         if not url:
#             return str(hash(datetime.utcnow().isoformat()))
        
#         # Try to extract ID from URL
#         match = re.search(r'/(\w+)/?$', url)
#         if match:
#             return match.group(1)
        
#         return str(hash(url))
    
#     async def save_jobs_to_supabase(self, jobs: List[Dict], table_name: str = 'jobs') -> bool:
#         """
#         Save job listings to Supabase.
        
#         Args:
#             jobs: List of job dictionaries
#             table_name: Supabase table name
#         """
#         if not jobs:
#             logger.info("No jobs to save")
#             return True
            
#         try:
#             # Insert jobs in batches to avoid API limits
#             batch_size = 50
            
#             for i in range(0, len(jobs), batch_size):
#                 batch = jobs[i:i + batch_size]
                
#                 # Use upsert to handle duplicates based on job_id and source
#                 result = self.supabase.table(table_name).upsert(
#                     batch,
#                     on_conflict='job_id,source'
#                 ).execute()
                
#                 logger.info(f"Saved batch {i//batch_size + 1}: {len(batch)} jobs")
            
#             logger.info(f"Successfully saved {len(jobs)} jobs to Supabase")
#             return True
            
#         except Exception as e:
#             logger.error(f"Error saving jobs to Supabase: {str(e)}")
#             return False
    
#     async def scrape_and_save(self, keywords: str, location: str = "", 
#                             pages: int = 5, table_name: str = 'jobs') -> Dict:
#         """
#         Complete scraping workflow: scrape both sites and save to Supabase.
        
#         Args:
#             keywords: Job search keywords
#             location: Job location
#             pages: Number of pages to scrape per site
#             table_name: Supabase table name
#         """
#         results = {
#             'indeed_jobs': 0,
#             'careerbuilder_jobs': 0,
#             'total_jobs': 0,
#             'success': False
#         }
        
#         try:
#             logger.info(f"Starting job scrape for: {keywords} in {location}")
            
#             # Scrape Indeed
#             indeed_jobs = await self.scrape_indeed_jobs(keywords, location, pages)
#             results['indeed_jobs'] = len(indeed_jobs)
            
#             # Scrape CareerBuilder
#             careerbuilder_jobs = await self.scrape_careerbuilder_jobs(keywords, location, pages)
#             results['careerbuilder_jobs'] = len(careerbuilder_jobs)
            
#             # Combine all jobs
#             all_jobs = indeed_jobs + careerbuilder_jobs
#             results['total_jobs'] = len(all_jobs)
            
#             # Save to Supabase
#             if all_jobs:
#                 save_success = await self.save_jobs_to_supabase(all_jobs, table_name)
#                 results['success'] = save_success
#             else:
#                 logger.warning("No jobs found to save")
#                 results['success'] = True
            
#             logger.info(f"Scraping complete: {results}")
#             return results
            
#         except Exception as e:
#             logger.error(f"Error in scrape_and_save: {str(e)}")
#             results['error'] = str(e)
#             return results


# # Example usage and setup
# async def main():
#     """Example usage of the JobScraper"""
    
#     # Your Supabase credentials
#     SUPABASE_URL = "your-supabase-url"
#     SUPABASE_KEY = "your-supabase-anon-key"
    
#     # Search parameters
#     keywords = "python developer"
#     location = "New York, NY"
#     pages = 3
    
#     async with JobScraper(SUPABASE_URL, SUPABASE_KEY) as scraper:
#         results = await scraper.scrape_and_save(
#             keywords=keywords,
#             location=location,
#             pages=pages,
#             table_name='jobs'
#         )
        
#         print(f"Scraping Results: {results}")


