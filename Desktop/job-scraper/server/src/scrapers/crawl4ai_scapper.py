# # File: backend/src/scrapers/crawl4ai_scraper.py
# import asyncio
# import json
# import time
# import random
# from typing import List, Dict, Optional
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
# from crawl4ai.extraction_strategy import LLMExtractionStrategy, JsonCssExtractionStrategy
# from supabase import create_client, Client
# import os
# from datetime import datetime
# # from src.scrapers.crawl4ai_scraper import Crawl4AIJobScraper
# from dotenv import load_dotenv
# load_dotenv()

# class Crawl4AIJobScraper:
#     """Advanced job scraper using Crawl4AI with Supabase integration"""
    
#     def __init__(self):
#         # Supabase setup
#         self.supabase_url = os.getenv("SUPABASE_URL")
#         self.supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
#         self.supabase: Client = create_client(self.supabase_url, self.supabase_key) # type: ignore
#         print("[INIT] Initialized Crawl4AIJobScraper")

#         # Browser configuration for stealth
#         self.browser_config = BrowserConfig(
#             headless=True,
#             browser_type="chromium",
#             use_persistent_context=True,
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#             viewport_width=1920,
#             viewport_height=1080,
#             accept_downloads=False,
#             java_script_enabled=True,
#             cookies=[],
#             headers={
#                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#                 "Accept-Language": "en-US,en;q=0.5",
#                 "Accept-Encoding": "gzip, deflate",
#                 "DNT": "1",
#                 "Connection": "keep-alive",
#                 "Upgrade-Insecure-Requests": "1",
#             }
#         )
        
#         # Job extraction schema
#         self.job_schema = {
#             "type": "object",
#             "properties": {
#                 "jobs": {
#                     "type": "array",
#                     "items": {
#                         "type": "object",
#                         "properties": {
#                             "title": {"type": "string"},
#                             "company": {"type": "string"},
#                             "location": {"type": "string"},
#                             "description": {"type": "string"},
#                             "salary": {"type": "string"},
#                             "job_type": {"type": "string"},
#                             "posted_date": {"type": "string"},
#                             "apply_url": {"type": "string"},
#                             "job_id": {"type": "string"}
#                         },
#                         "required": ["title", "company", "location"]
#                     }
#                 }
#             }
#         }
    
#     async def scrape_indeed(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
#         """Scrape Indeed using Crawl4AI"""
#         jobs = []

#         async with AsyncWebCrawler(config=self.browser_config) as crawler:
#             for page in range(pages):
#                 try:
#                     # Build Indeed search URL
#                     base_url = "https://www.indeed.com/jobs"
#                     params = f"?q={keywords.replace(' ', '+')}&start={page * 10}"
#                     if location:
#                         params += f"&l={location.replace(' ', '+')}"
                    
#                     url = base_url + params
                    
#                     # CSS selectors for Indeed job data
#                     # css_extraction_config = {
#                     #     "jobs": [
#                     #         {
#                     #             "selector": "[data-testid='slider_item']",
#                     #             "fields": {
#                     #                 "title": {"selector": "[data-testid='job-title'] span", "attribute": "text"},
#                     #                 "company": {"selector": "[data-testid='company-name']", "attribute": "text"},
#                     #                 "location": {"selector": "[data-testid='job-location']", "attribute": "text"},
#                     #                 "salary": {"selector": "[data-testid='salary-snippet']", "attribute": "text"},
#                     #                 "job_type": {"selector": "[data-testid='job-snippet'] span", "attribute": "text"},
#                     #                 "apply_url": {"selector": "[data-testid='job-title'] a", "attribute": "href"},
#                     #                 "job_id": {"selector": "", "attribute": "data-jk"},
#                     #                 "posted_date": {"selector": "[data-testid='myJobsStateDate']", "attribute": "text"}
#                     #             }
#                     #         }
#                     #     ]
#                     # }
#                     css_extraction_config = {
#                         "baseSelector": ".job-search-card",
#                         "fields": {
#                             "title": {"selector": ".base-search-card__title", "attribute": "text"},
#                             "company": {"selector": ".base-search-card__subtitle", "attribute": "text"},
#                             "location": {"selector": ".job-search-card__location", "attribute": "text"},
#                             "apply_url": {"selector": ".base-card__full-link", "attribute": "href"},
#                             "posted_date": {"selector": ".job-search-card__listdate", "attribute": "text"}
#                         }
#                     }

#                     extraction_strategy = JsonCssExtractionStrategy(css_extraction_config)
                    
#                     # Configure crawler run
#                     # run_config = CrawlerRunConfig(
#                     #     extraction_strategy=extraction_strategy,
#                     #     js_code="""
#                     #     // Hide webdriver property
#                     #     Object.defineProperty(navigator, 'webdriver', {
#                     #         get: () => undefined,
#                     #     });
                        
#                     #     // Simulate human behavior
#                     #     setTimeout(() => {
#                     #         window.scrollTo(0, Math.floor(Math.random() * 500));
#                     #     }, Math.random() * 2000);
#                     #     """,
#                     #     wait_for="css:[data-testid='job-title']",
#                     #     page_timeout=30000,
#                     #     delay_before_return_html=random.uniform(2, 5)
#                     # )
#                     run_config = CrawlerRunConfig(
#                         extraction_strategy=JsonCssExtractionStrategy(css_extraction_config),
#                         js_code="""
#                             Object.defineProperty(navigator, 'webdriver', {
#                                 get: () => undefined,
#                             });
#                             setTimeout(() => { window.scrollTo(0, Math.floor(Math.random() * 500)); }, Math.random() * 2000);
#                         """,
#                         wait_for="[data-testid='slider_item']",  # Make sure this is the container selector, not empty
#                         page_timeout=30000,
#                         delay_before_return_html=random.uniform(2, 5)
#                     )
#                     # Crawl the page
#                     result = await crawler.arun(url=url, config=run_config)
                    
#                     if result.success and result.extracted_content: # type: ignore
#                         extracted_data = json.loads(result.extracted_content) # type: ignore
#                         page_jobs = extracted_data.get("jobs", [])
                        
#                         for job in page_jobs:
#                             if job.get("title") and job.get("company"):
#                                 job["source"] = "Indeed"
#                                 job["scraped_at"] = datetime.utcnow().isoformat()
#                                 job["keywords"] = keywords
#                                 jobs.append(job)
                    
#                     # Random delay between pages
#                     await asyncio.sleep(random.uniform(3, 7))
                    
#                 except Exception as e:
#                     print(f"Error scraping Indeed page {page}: {e}")
#                     continue
#         print(f"[SCRAPE_INDEED] Starting scrape for: {keywords}, page: {page}")
        
#         return jobs
    
#     async def scrape_linkedin(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
#         """Scrape LinkedIn using Crawl4AI"""
#         jobs = []
        
#         async with AsyncWebCrawler(config=self.browser_config) as crawler:
#             for page in range(pages):
#                 try:
#                     # LinkedIn search URL (note: requires careful handling due to authentication)
#                     base_url = "https://www.linkedin.com/jobs/search"
#                     params = f"?keywords={keywords.replace(' ', '%20')}&start={page * 25}"
#                     if location:
#                         params += f"&location={location.replace(' ', '%20')}"
                    
#                     url = base_url + params
                    
#                     # CSS selectors for LinkedIn
#                     css_extraction_config = {
#                         "baseSelector": ".job-search-card",
#                         "fields": {
#                             "title": {"selector": ".base-search-card__title", "attribute": "text"},
#                             "company": {"selector": ".base-search-card__subtitle", "attribute": "text"},
#                             "location": {"selector": ".job-search-card__location", "attribute": "text"},
#                             "apply_url": {"selector": ".base-card__full-link", "attribute": "href"},
#                             "posted_date": {"selector": ".job-search-card__listdate", "attribute": "text"}
#                         }
#                     }

                    
#                     extraction_strategy = JsonCssExtractionStrategy(css_extraction_config)
                    
#                     run_config = CrawlerRunConfig(
#                         extraction_strategy=extraction_strategy,
#                         js_code="""
#                         // Anti-detection measures
#                         Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#                         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
#                         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
#                         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
#                         """,
#                         wait_for="css:.job-search-card",
#                         page_timeout=30000,
#                         delay_before_return_html=random.uniform(3, 6)
#                     )
                    
#                     result = await crawler.arun(url=url, config=run_config)
                    
#                     if result.success and result.extracted_content: # type: ignore
#                         extracted_data = json.loads(result.extracted_content) # type: ignore
#                         page_jobs = extracted_data.get("jobs", [])
                        
#                         for job in page_jobs:
#                             if job.get("title") and job.get("company"):
#                                 job["source"] = "LinkedIn"
#                                 job["scraped_at"] = datetime.utcnow().isoformat()
#                                 job["keywords"] = keywords
#                                 jobs.append(job)
                    
#                     await asyncio.sleep(random.uniform(4, 8))
                    
#                 except Exception as e:
#                     print(f"Error scraping LinkedIn page {page}: {e}")
#                     continue
        
#         return jobs
    
#     async def scrape_glassdoor(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
#         """Scrape Glassdoor using Crawl4AI"""
#         jobs = []
        
#         async with AsyncWebCrawler(config=self.browser_config) as crawler:
#             for page in range(pages):
#                 try:
#                     # Glassdoor search URL
#                     base_url = "https://www.glassdoor.com/Job/jobs.htm"
#                     params = f"?sc.keyword={keywords.replace(' ', '+')}&p={page + 1}"
#                     if location:
#                         params += f"&locT=C&locId={location.replace(' ', '+')}"
                    
#                     url = base_url + params
                    
#                     css_extraction_config = {
#                         "baseSelector": ".job-search-card",
#                         "fields": {
#                             "title": {"selector": ".base-search-card__title", "attribute": "text"},
#                             "company": {"selector": ".base-search-card__subtitle", "attribute": "text"},
#                             "location": {"selector": ".job-search-card__location", "attribute": "text"},
#                             "apply_url": {"selector": ".base-card__full-link", "attribute": "href"},
#                             "posted_date": {"selector": ".job-search-card__listdate", "attribute": "text"}
#                         }
#                     }

                    
#                     extraction_strategy = JsonCssExtractionStrategy(css_extraction_config)
                    
#                     run_config = CrawlerRunConfig(
#                         extraction_strategy=extraction_strategy,
#                         js_code="""
#                         // Glassdoor anti-detection
#                         Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#                         window.chrome = {runtime: {}};
#                         """,
#                         wait_for="css:[data-test='jobListing']",
#                         page_timeout=30000,
#                         delay_before_return_html=random.uniform(2, 5)
#                     )
                    
#                     result = await crawler.arun(url=url, config=run_config)
                    
#                     if result.success and result.extracted_content: # type: ignore
#                         extracted_data = json.loads(result.extracted_content) # type: ignore
#                         page_jobs = extracted_data.get("jobs", [])
                        
#                         for job in page_jobs:
#                             if job.get("title") and job.get("company"):
#                                 job["source"] = "Glassdoor"
#                                 job["scraped_at"] = datetime.utcnow().isoformat()
#                                 job["keywords"] = keywords
#                                 jobs.append(job)
                    
#                     await asyncio.sleep(random.uniform(3, 6))
                    
#                 except Exception as e:
#                     print(f"Error scraping Glassdoor page {page}: {e}")
#                     continue
        
#         return jobs
    
#     def save_jobs_to_supabase(self, jobs: List[Dict], user_id: str = None) -> bool: # type: ignore
#         """Save scraped jobs to Supabase"""
#         print(f"[SAVE] Attempting to save {len(jobs)} jobs to Supabase")

#         try:
#             for job in jobs:
#                 # Check if job already exists
#                 existing = self.supabase.table("jobs").select("id").eq("job_id", job.get("job_id", "")).eq("source", job["source"]).execute()
                
#                 if not existing.data:
#                     # Prepare job data for insertion
#                     job_data = {
#                         "title": job.get("title", ""),
#                         "company": job.get("company", ""),
#                         "location": job.get("location", ""),
#                         "description": job.get("description", ""),
#                         "salary": job.get("salary", ""),
#                         "job_type": job.get("job_type", ""),
#                         "posted_date": job.get("posted_date", ""),
#                         "apply_url": job.get("apply_url", ""),
#                         "job_id": job.get("job_id", ""),
#                         "source": job["source"],
#                         "keywords": job["keywords"],
#                         "scraped_at": job["scraped_at"],
#                         "user_id": user_id
#                     }
                    
#                     # Insert into Supabase
#                     result = self.supabase.table("jobs").insert(job_data).execute()
                    
#                     if result.data:
#                         print(f"Saved job: {job['title']} at {job['company']}")
            
#             return True
            
#         except Exception as e:
#             print(f"Error saving jobs to Supabase: {e}")
#             return False
    
#     def get_user_keywords(self, user_id: str) -> List[str]:
#         """Get user's search keywords from Supabase"""
#         try:
#             result = self.supabase.table("user_keywords").select("keyword").eq("user_id", user_id).execute()
#             return [row["keyword"] for row in result.data]
#         except Exception as e:
#             print(f"Error fetching user keywords: {e}")
#             return []
    
#     async def run_full_scrape(self, user_id: str = None, keywords: List[str] = None) -> Dict: # type: ignore
#         """Run full scraping process for all sites"""
#         if not keywords:
#             keywords = self.get_user_keywords(user_id) if user_id else ["software engineer", "web developer"]
        
#         all_jobs = []
#         scrape_results = {
#             "total_jobs": 0,
#             "sites_scraped": [],
#             "keywords_used": keywords,
#             "timestamp": datetime.utcnow().isoformat()
#         }
        
#         for keyword in keywords:
#             print(f"Scraping for keyword: {keyword}")
            
#             # Scrape Indeed
#             try:
#                 indeed_jobs = await self.scrape_indeed(keyword, pages=2)
#                 all_jobs.extend(indeed_jobs)
#                 scrape_results["sites_scraped"].append(f"Indeed ({len(indeed_jobs)} jobs)")
#                 print(f"Found {len(indeed_jobs)} jobs on Indeed for '{keyword}'")
#             except Exception as e:
#                 print(f"Error scraping Indeed for '{keyword}': {e}")
            
#             # Scrape LinkedIn
#             try:
#                 linkedin_jobs = await self.scrape_linkedin(keyword, pages=2)
#                 all_jobs.extend(linkedin_jobs)
#                 scrape_results["sites_scraped"].append(f"LinkedIn ({len(linkedin_jobs)} jobs)")
#                 print(f"Found {len(linkedin_jobs)} jobs on LinkedIn for '{keyword}'")
#             except Exception as e:
#                 print(f"Error scraping LinkedIn for '{keyword}': {e}")
            
#             # Scrape Glassdoor
#             try:
#                 glassdoor_jobs = await self.scrape_glassdoor(keyword, pages=2)
#                 all_jobs.extend(glassdoor_jobs)
#                 scrape_results["sites_scraped"].append(f"Glassdoor ({len(glassdoor_jobs)} jobs)")
#                 print(f"Found {len(glassdoor_jobs)} jobs on Glassdoor for '{keyword}'")
#             except Exception as e:
#                 print(f"Error scraping Glassdoor for '{keyword}': {e}")
            
#             # Delay between keywords
#             await asyncio.sleep(random.uniform(5, 10))
        
#         # Save all jobs to Supabase
#         if all_jobs:
#             success = self.save_jobs_to_supabase(all_jobs, user_id)
#             scrape_results["total_jobs"] = len(all_jobs)
#             scrape_results["saved_to_db"] = success
#         print(f"[COMPLETE] Scrape finished. Total jobs: {scrape_results['total_jobs']}")
#         results_dir = "scrape_output"
#         os.makedirs(results_dir, exist_ok=True)
#         timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
#         output_file = os.path.join(results_dir, f"scrape_results_{timestamp}.json")

#         with open(output_file, "w", encoding="utf-8") as f:
#             json.dump(scrape_results, f, indent=4)

#         print(f"[MAIN] Results saved to {output_file}")
#         return scrape_results
# if __name__ == "__main__":
#     import asyncio
#     # from scrapers.crawl4ai_scraper import Crawl4AIJobScraper

#     print("[MAIN] Starting scraper")

#     scraper = Crawl4AIJobScraper()

#     # Run the full scrape (you can hardcode a test keyword list or pass a test user_id)
#     asyncio.run(scraper.run_full_scrape(keywords=["python developer", "ai engineer"]))
# File: backend/src/scrapers/crawl4ai_scraper.py
import asyncio
import json
import time
import random
from typing import List, Dict, Optional
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy, JsonCssExtractionStrategy
from supabase import create_client, Client
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()
from utils.selenium_utils import StealthDriver


class Crawl4AIJobScraper:
    """Advanced job scraper using Crawl4AI with Supabase integration"""
    
    def __init__(self):
        # Supabase setup
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key) # type: ignore
        print("[INIT] Initialized Crawl4AIJobScraper")

        # Browser configuration for stealth
        self.browser_config = BrowserConfig(
            headless=True,
            browser_type="chromium",
            use_persistent_context=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport_width=1920,
            viewport_height=1080,
            accept_downloads=False,
            java_script_enabled=True,
            cookies=[],
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )
    
    async def scrape_indeed(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
        """Scrape Indeed using Crawl4AI"""
        jobs = []

        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for page in range(pages):
                try:
                    print(f"[SCRAPE_INDEED] Starting scrape for: {keywords}, page: {page}")
                    
                    # Build Indeed search URL
                    base_url = "https://www.indeed.com/jobs"
                    params = f"?q={keywords.replace(' ', '+')}&start={page * 10}"
                    if location:
                        params += f"&l={location.replace(' ', '+')}"
                    
                    url = base_url + params
                    
                    # Fixed CSS selectors for Indeed job data
                    css_extraction_config = {
                        "name": "indeed_jobs",
                        "baseSelector": ".slider_container .slider_item, .job_seen_beacon",
                        "fields": [
                            {
                                "name": "title",
                                "selector": "h2.jobTitle a span, .jobTitle a",
                                "attribute": "text"
                            },
                            {
                                "name": "company", 
                                "selector": ".companyName a, .companyName",
                                "attribute": "text"
                            },
                            {
                                "name": "location",
                                "selector": ".companyLocation",
                                "attribute": "text"
                            },
                            {
                                "name": "salary",
                                "selector": ".salary-snippet",
                                "attribute": "text"
                            },
                            {
                                "name": "apply_url",
                                "selector": "h2.jobTitle a",
                                "attribute": "href"
                            },
                            {
                                "name": "job_id",
                                "selector": "",
                                "attribute": "data-jk"
                            },
                            {
                                "name": "posted_date",
                                "selector": ".date",
                                "attribute": "text"
                            }
                        ]
                    }

                    extraction_strategy = JsonCssExtractionStrategy(css_extraction_config)
                    
                    # Configure crawler run with proper wait selector
                    run_config = CrawlerRunConfig(
                        extraction_strategy=extraction_strategy,
                        js_code="""
                        // Hide webdriver property
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined,
                        });
                        
                        // Remove other automation indicators
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                        
                        // Simulate human behavior
                        setTimeout(() => {
                            window.scrollTo(0, Math.floor(Math.random() * 500));
                        }, Math.random() * 2000);
                        """,
                        wait_for="css:.jobTitle, .slider_item",
                        page_timeout=30000,
                        delay_before_return_html=random.uniform(2, 5)
                    )
                    
                    # Crawl the page
                    result = await crawler.arun(url=url, config=run_config)
                    
                    if result.success and result.extracted_content: # type: ignore
                        try:
                            extracted_data = json.loads(result.extracted_content) # type: ignore
                            
                            # Handle the extracted data structure properly
                            if isinstance(extracted_data, list):
                                page_jobs = extracted_data
                            elif isinstance(extracted_data, dict) and "indeed_jobs" in extracted_data:
                                page_jobs = extracted_data["indeed_jobs"]
                            else:
                                page_jobs = []
                            
                            for job in page_jobs:
                                if isinstance(job, dict) and job.get("title") and job.get("company"):
                                    # Clean and format the job data
                                    clean_job = {
                                        "title": job.get("title", "").strip(),
                                        "company": job.get("company", "").strip(),
                                        "location": job.get("location", "").strip(),
                                        "description": job.get("description", ""),
                                        "salary": job.get("salary", "").strip(),
                                        "job_type": job.get("job_type", ""),
                                        "posted_date": job.get("posted_date", "").strip(),
                                        "apply_url": job.get("apply_url", ""),
                                        "job_id": job.get("job_id", f"indeed_{hash(job.get('title', '') + job.get('company', ''))}"),
                                        "source": "Indeed",
                                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                                        "keywords": keywords
                                    }
                                    jobs.append(clean_job)
                                    
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON from Indeed: {e}")
                            continue
                    
                    # Random delay between pages
                    await asyncio.sleep(random.uniform(3, 7))
                    
                except Exception as e:
                    print(f"Error scraping Indeed page {page}: {e}")
                    continue
        
        return jobs
    
    async def scrape_linkedin(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
        """Scrape LinkedIn using Crawl4AI"""
        jobs = []
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for page in range(pages):
                try:
                    print(f"[SCRAPE_LINKEDIN] Starting scrape for: {keywords}, page: {page}")
                    
                    # LinkedIn search URL
                    base_url = "https://www.linkedin.com/jobs/search"
                    params = f"?keywords={keywords.replace(' ', '%20')}&start={page * 25}"
                    if location:
                        params += f"&location={location.replace(' ', '%20')}"
                    
                    url = base_url + params
                    
                    # Fixed CSS selectors for LinkedIn
                    css_extraction_config = {
                        "name": "linkedin_jobs",
                        "baseSelector": ".job-search-card, .base-card",
                        "fields": [
                            {
                                "name": "title",
                                "selector": ".base-search-card__title, .job-search-card__title a",
                                "attribute": "text"
                            },
                            {
                                "name": "company",
                                "selector": ".base-search-card__subtitle, .job-search-card__subtitle a",
                                "attribute": "text"
                            },
                            {
                                "name": "location",
                                "selector": ".job-search-card__location",
                                "attribute": "text"
                            },
                            {
                                "name": "apply_url",
                                "selector": ".base-card__full-link, .job-search-card__title a",
                                "attribute": "href"
                            },
                            {
                                "name": "posted_date",
                                "selector": ".job-search-card__listdate",
                                "attribute": "text"
                            }
                        ]
                    }
                    
                    extraction_strategy = JsonCssExtractionStrategy(css_extraction_config)
                    
                    run_config = CrawlerRunConfig(
                        extraction_strategy=extraction_strategy,
                        js_code="""
                        // Anti-detection measures
                        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                        
                        // Simulate human behavior
                        setTimeout(() => {
                            window.scrollTo(0, Math.floor(Math.random() * 1000));
                        }, Math.random() * 3000);
                        """,
                        wait_for="css:.job-search-card, .base-card",
                        page_timeout=30000,
                        delay_before_return_html=random.uniform(3, 6)
                    )
                    
                    result = await crawler.arun(url=url, config=run_config)
                    
                    if result.success and result.extracted_content: # type: ignore
                        try:
                            extracted_data = json.loads(result.extracted_content) # type: ignore
                            
                            # Handle the extracted data structure properly
                            if isinstance(extracted_data, list):
                                page_jobs = extracted_data
                            elif isinstance(extracted_data, dict) and "linkedin_jobs" in extracted_data:
                                page_jobs = extracted_data["linkedin_jobs"]
                            else:
                                page_jobs = []
                            
                            for job in page_jobs:
                                if isinstance(job, dict) and job.get("title") and job.get("company"):
                                    clean_job = {
                                        "title": job.get("title", "").strip(),
                                        "company": job.get("company", "").strip(),
                                        "location": job.get("location", "").strip(),
                                        "description": job.get("description", ""),
                                        "salary": job.get("salary", ""),
                                        "job_type": job.get("job_type", ""),
                                        "posted_date": job.get("posted_date", "").strip(),
                                        "apply_url": job.get("apply_url", ""),
                                        "job_id": job.get("job_id", f"linkedin_{hash(job.get('title', '') + job.get('company', ''))}"),
                                        "source": "LinkedIn",
                                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                                        "keywords": keywords
                                    }
                                    jobs.append(clean_job)
                                    
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON from LinkedIn: {e}")
                            continue
                    
                    await asyncio.sleep(random.uniform(4, 8))
                    
                except Exception as e:
                    print(f"Error scraping LinkedIn page {page}: {e}")
                    continue
        
        return jobs
    
    async def scrape_glassdoor(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
        """Scrape Glassdoor using Crawl4AI"""
        jobs = []
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for page in range(pages):
                try:
                    print(f"[SCRAPE_GLASSDOOR] Starting scrape for: {keywords}, page: {page}")
                    
                    # Glassdoor search URL
                    base_url = "https://www.glassdoor.com/Job/jobs.htm"
                    params = f"?sc.keyword={keywords.replace(' ', '+')}&p={page + 1}"
                    if location:
                        params += f"&locT=C&locId={location.replace(' ', '+')}"
                    
                    url = base_url + params
                    
                    # Fixed CSS selectors for Glassdoor
                    css_extraction_config = {
                        "name": "glassdoor_jobs",
                        "baseSelector": "[data-test='jobListing'], .jobListing",
                        "fields": [
                            {
                                "name": "title",
                                "selector": "[data-test='job-title'], .jobTitle",
                                "attribute": "text"
                            },
                            {
                                "name": "company",
                                "selector": "[data-test='employer-name'], .employerName",
                                "attribute": "text"
                            },
                            {
                                "name": "location",
                                "selector": "[data-test='job-location'], .jobLocation",
                                "attribute": "text"
                            },
                            {
                                "name": "salary",
                                "selector": "[data-test='detailSalary'], .salaryText",
                                "attribute": "text"
                            },
                            {
                                "name": "apply_url",
                                "selector": "[data-test='job-title'] a, .jobTitle a",
                                "attribute": "href"
                            }
                        ]
                    }
                    
                    extraction_strategy = JsonCssExtractionStrategy(css_extraction_config)
                    
                    run_config = CrawlerRunConfig(
                        extraction_strategy=extraction_strategy,
                        js_code="""
                        // Glassdoor anti-detection
                        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                        window.chrome = {runtime: {}};
                        
                        // Remove automation indicators
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                        
                        // Simulate human behavior
                        setTimeout(() => {
                            window.scrollTo(0, Math.floor(Math.random() * 800));
                        }, Math.random() * 2500);
                        """,
                        wait_for="css:[data-test='jobListing'], .jobListing",
                        page_timeout=30000,
                        delay_before_return_html=random.uniform(2, 5)
                    )
                    
                    result = await crawler.arun(url=url, config=run_config)
                    
                    if result.success and result.extracted_content: # type: ignore
                        try:
                            extracted_data = json.loads(result.extracted_content) # type: ignore
                            
                            # Handle the extracted data structure properly
                            if isinstance(extracted_data, list):
                                page_jobs = extracted_data
                            elif isinstance(extracted_data, dict) and "glassdoor_jobs" in extracted_data:
                                page_jobs = extracted_data["glassdoor_jobs"]
                            else:
                                page_jobs = []
                            
                            for job in page_jobs:
                                if isinstance(job, dict) and job.get("title") and job.get("company"):
                                    clean_job = {
                                        "title": job.get("title", "").strip(),
                                        "company": job.get("company", "").strip(),
                                        "location": job.get("location", "").strip(),
                                        "description": job.get("description", ""),
                                        "salary": job.get("salary", "").strip(),
                                        "job_type": job.get("job_type", ""),
                                        "posted_date": job.get("posted_date", ""),
                                        "apply_url": job.get("apply_url", ""),
                                        "job_id": job.get("job_id", f"glassdoor_{hash(job.get('title', '') + job.get('company', ''))}"),
                                        "source": "Glassdoor",
                                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                                        "keywords": keywords
                                    }
                                    jobs.append(clean_job)
                                    
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON from Glassdoor: {e}")
                            continue
                    
                    await asyncio.sleep(random.uniform(3, 6))
                    
                except Exception as e:
                    print(f"Error scraping Glassdoor page {page}: {e}")
                    continue
        
        return jobs
    
    def save_jobs_to_supabase(self, jobs: List[Dict], user_id: str = None) -> bool: # type: ignore
        """Save scraped jobs to Supabase"""
        print(f"[SAVE] Attempting to save {len(jobs)} jobs to Supabase")

        try:
            for job in jobs:
                # Check if job already exists
                existing = self.supabase.table("jobs").select("id").eq("job_id", job.get("job_id", "")).eq("source", job["source"]).execute()
                
                if not existing.data:
                    # Prepare job data for insertion
                    job_data = {
                        "title": job.get("title", ""),
                        "company": job.get("company", ""),
                        "location": job.get("location", ""),
                        "description": job.get("description", ""),
                        "salary": job.get("salary", ""),
                        "job_type": job.get("job_type", ""),
                        "posted_date": job.get("posted_date", ""),
                        "apply_url": job.get("apply_url", ""),
                        "job_id": job.get("job_id", ""),
                        "source": job["source"],
                        "keywords": job["keywords"],
                        "scraped_at": job["scraped_at"],
                        "user_id": user_id
                    }
                    
                    # Insert into Supabase
                    result = self.supabase.table("jobs").insert(job_data).execute()
                    
                    if result.data:
                        print(f"Saved job: {job['title']} at {job['company']}")
                else:
                    print(f"Job already exists: {job['title']} at {job['company']}")
            
            return True
            
        except Exception as e:
            print(f"Error saving jobs to Supabase: {e}")
            return False
    
    def get_user_keywords(self, user_id: str) -> List[str]:
        """Get user's search keywords from Supabase"""
        try:
            result = self.supabase.table("user_keywords").select("keyword").eq("user_id", user_id).execute()
            return [row["keyword"] for row in result.data]
        except Exception as e:
            print(f"Error fetching user keywords: {e}")
            return []
    
    async def run_full_scrape(self, user_id: str = None, keywords: List[str] = None) -> Dict: # type: ignore
        """Run full scraping process for all sites"""
        if not keywords:
            keywords = self.get_user_keywords(user_id) if user_id else ["software engineer", "web developer"]
        
        all_jobs = []
        scrape_results = {
            "total_jobs": 0,
            "sites_scraped": [],
            "keywords_used": keywords,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        for keyword in keywords:
            print(f"Scraping for keyword: {keyword}")
            
            # Scrape Indeed
            try:
                indeed_jobs = await self.scrape_indeed(keyword, pages=2)
                all_jobs.extend(indeed_jobs)
                scrape_results["sites_scraped"].append(f"Indeed ({len(indeed_jobs)} jobs)")
                print(f"Found {len(indeed_jobs)} jobs on Indeed for '{keyword}'")
            except Exception as e:
                print(f"Error scraping Indeed for '{keyword}': {e}")
            
            # Scrape LinkedIn
            try:
                linkedin_jobs = await self.scrape_linkedin(keyword, pages=2)
                all_jobs.extend(linkedin_jobs)
                scrape_results["sites_scraped"].append(f"LinkedIn ({len(linkedin_jobs)} jobs)")
                print(f"Found {len(linkedin_jobs)} jobs on LinkedIn for '{keyword}'")
            except Exception as e:
                print(f"Error scraping LinkedIn for '{keyword}': {e}")
            
            # Scrape Glassdoor
            try:
                glassdoor_jobs = await self.scrape_glassdoor(keyword, pages=2)
                all_jobs.extend(glassdoor_jobs)
                scrape_results["sites_scraped"].append(f"Glassdoor ({len(glassdoor_jobs)} jobs)")
                print(f"Found {len(glassdoor_jobs)} jobs on Glassdoor for '{keyword}'")
            except Exception as e:
                print(f"Error scraping Glassdoor for '{keyword}': {e}")
            
            # Delay between keywords
            await asyncio.sleep(random.uniform(5, 10))
        
        # Save all jobs to Supabase
        if all_jobs:
            success = self.save_jobs_to_supabase(all_jobs, user_id)
            scrape_results["total_jobs"] = len(all_jobs)
            scrape_results["saved_to_db"] = success
        
        print(f"[COMPLETE] Scrape finished. Total jobs: {scrape_results['total_jobs']}")
        
        # Save results to file
        results_dir = "scrape_output"
        os.makedirs(results_dir, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(results_dir, f"scrape_results_{timestamp}.json")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(scrape_results, f, indent=4)

        print(f"[MAIN] Results saved to {output_file}")
        return scrape_results

if __name__ == "__main__":
    import asyncio

    print("[MAIN] Starting scraper")

    scraper = Crawl4AIJobScraper()

    # Run the full scrape (you can hardcode a test keyword list or pass a test user_id)
    asyncio.run(scraper.run_full_scrape(keywords=["python developer", "ai engineer"]))