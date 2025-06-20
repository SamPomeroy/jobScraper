import requests
from bs4 import BeautifulSoup
import json
import datetime
from urllib.parse import urljoin
from dotenv import load_dotenv
import os
from bs4.element import Tag


# load_dotenv()

# BASE_URL = os.getenv("INDEED_URL", "https://www.indeed.com/jobs?q=junior+developer&l=remote")
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
# }

# def scrape_indeed_jobs():
#     print("Scraping Indeed for jobs...")

#     response = requests.get(BASE_URL, headers=HEADERS)
#     print("Status Code:", response.status_code)
#     print("First 500 chars of HTML:\n", response.text[:500])  # Inspect this

#     soup = BeautifulSoup(response.text, 'html.parser')
#     job_cards = soup.find_all('a', class_='tapItem')
#     print(f"Found {len(job_cards)} <a class='tapItem'> elements.")

#     jobs = []
#     for card in job_cards:
#         try:
#             title_elem = card.find('h2', class_='jobTitle')
#             company_elem = card.find('span', class_='companyName')
#             summary_elem = card.find('div', class_='job-snippet')
#             href = card.get('href')
#             if not href or not isinstance(card, Tag):
#                 continue
#             link = urljoin("https://www.indeed.com", href)
#             if not title_elem or not company_elem:
#                 continue

#             job = {
#                 "title": title_elem.get_text(strip=True),
#                 "company": company_elem.get_text(strip=True),
#                 "summary": summary_elem.get_text(strip=True) if summary_elem else "",
#                 "link": link,
#                 "timestamp": datetime.datetime.now().isoformat()
#             }
#             jobs.append(job)
#         except Exception as e:
#             print(f"Error parsing job card: {e}")
#             continue

#     print(f"✅ Parsed {len(jobs)} job postings.")
#     return jobs

# if __name__ == "__main__":
#     results = scrape_indeed_jobs()
#     with open("data/indeed_jobs.json", "w") as f:
#         json.dump(results, f, indent=2)
#     print("Saved to data/indeed_jobs.json ✅")
# import requests
# from bs4 import BeautifulSoup, Tag
# import json
# import datetime
# from urllib.parse import urljoin
# from dotenv import load_dotenv
# import os

# load_dotenv()

# BASE_URL = os.getenv("INDEED_URL", "https://www.indeed.com/jobs?q=junior+developer&l=remote")
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
# }

# def scrape_indeed_jobs():
#     print("Scraping Indeed for jobs...")

#     response = requests.get(BASE_URL, headers=HEADERS)
#     print("Status Code:", response.status_code)
#     print("First 500 chars of HTML:\n", response.text[:500])  # Inspect this

#     soup = BeautifulSoup(response.text, 'html.parser')
#     job_cards = soup.find_all('a', class_='tapItem')
#     print(f"Found {len(job_cards)} <a class='tapItem'> elements.")

#     jobs = []
#     for card in job_cards:
#         if not isinstance(card, Tag):
#             continue  # Skip if not a Tag

#         try:
#             title_elem = card.find('h2', attrs={"class": "jobTitle"})
#             company_elem = card.find('span', attrs={"class": "companyName"})
#             summary_elem = card.find('div', attrs={"class": "job-snippet"})
#             href = card.get('href')

#             if not href:
#                 continue

#             link = urljoin("https://www.indeed.com", str(href))

#             if not title_elem or not company_elem:
#                 continue

#             job = {
#                 "title": title_elem.get_text(strip=True),
#                 "company": company_elem.get_text(strip=True),
#                 "summary": summary_elem.get_text(strip=True) if summary_elem else "",
#                 "link": link,
#                 "timestamp": datetime.datetime.now().isoformat()
#             }
#             jobs.append(job)
#         except Exception as e:
#             print(f"Error parsing job card: {e}")
#             continue

#     print(f"✅ Parsed {len(jobs)} job postings.")
#     return jobs

# if __name__ == "__main__":
#     results = scrape_indeed_jobs()
#     os.makedirs("data", exist_ok=True)
#     with open("data/indeed_jobs.json", "w") as f:
#         json.dump(results, f, indent=2)
#     print("Saved to data/indeed_jobs.json ✅")
# # File: backend/src/scrapers/indeed_scraper.py
# class IndeedScraper(BaseScraper):
#     """Indeed job scraper with advanced bot detection bypass"""
    
#     def __init__(self, headless: bool = True):
#         super().__init__(headless)
#         self.base_url = "https://www.indeed.com"
    
#     def search_jobs(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
#         """Search Indeed for jobs"""
#         if not self.setup_driver():
#             return []
        
#         jobs = []
        
#         try:
#             # Build search URL
#             search_url = f"{self.base_url}/jobs?q={keywords.replace(' ', '+')}"
#             if location:
#                 search_url += f"&l={location.replace(' ', '+')}"
            
#             for page in range(pages):
#                 page_url = f"{search_url}&start={page * 10}"
                
#                 if not self.safe_navigate(page_url):
#                     continue
                
#                 # Wait for job listings to load
#                 job_cards = self.stealth_driver.wait_and_find_element(
#                     self.driver, By.CSS_SELECTOR, "[data-testid='job-title']"
#                 )
                
#                 if not job_cards:
#                     continue
                
#                 # Find all job cards
#                 if self.driver is not None:
#                     job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
                    
#                     for job_elem in job_elements:
#                         try:
#                             job_data = self.extract_job_data(job_elem)
#                             if job_data:
#                                 jobs.append(job_data)
#                         except Exception as e:
#                             print(f"Error extracting job data: {e}")
#                             continue
#                 else:
#                     print("Driver is not initialized. Skipping job extraction for this page.")
                
#                 # Random delay between pages
#                 time.sleep(random.uniform(3, 7))
        
#         except Exception as e:
#             print(f"Error scraping Indeed: {e}")
        
#         finally:
#             self.cleanup()
        
#         return jobs
    
#     def extract_job_data(self, job_element) -> Dict:
#         """Extract job data from Indeed job card"""
#         try:
#             # Title
#             try:
#                 title_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-title'] span")
#                 title = title_elem.get_attribute("title") or title_elem.text
#             except Exception:
#                 title = ""

#             # Company
#             try:
#                 company_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='company-name'] span")
#                 company = company_elem.get_attribute("title") or company_elem.text
#             except Exception:
#                 company = ""

#             # Location
#             try:
#                 location_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-location']")
#                 location = location_elem.text
#             except Exception:
#                 location = ""

#             # Link
#             try:
#                 link_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-title'] a")
#                 job_link = link_elem.get_attribute("href")
#             except Exception:
#                 job_link = ""

#             # Job ID
#             try:
#                 job_id = job_element.get_attribute("data-jk")
#             except Exception:
#                 job_id = ""

#             if not (title and company and job_link):
#                 return None # type: ignore

#             return {
#                 "id": job_id,
#                 "title": title,
#                 "company": company,
#                 "location": location,
#                 "link": job_link,
#                 "source": "Indeed",
#                 "scraped_at": time.time()
#             }

#         except Exception as e:
#             print(f"Error extracting job data: {e}")
#             return None # type: ignore

# # Example usage
# if __name__ == "__main__":
#     scraper = IndeedScraper(headless=False)  # Set to True for production
#     jobs = scraper.search_jobs("software engineer", "San Francisco", pages=2)
    
#     for job in jobs:
#         print(f"Title: {job['title']}")
#         print(f"Company: {job['company']}")
#         print(f"Location: {job['location']}")
#         print(f"Link: {job['link']}")
#         print("-" * 50)







# File: backend/src/scrapers/indeed_scraper.py
class IndeedScraper(BaseScraper):
    """Indeed job scraper with advanced bot detection bypass"""
    
    def __init__(self, headless: bool = True):
        super().__init__(headless)
        self.base_url = "https://www.indeed.com"
    
    def search_jobs(self, keywords: str, location: str = "", pages: int = 3) -> List[Dict]:
        """Search Indeed for jobs"""
        if not self.setup_driver():
            return []
        
        jobs = []
        
        try:
            # Build search URL
            search_url = f"{self.base_url}/jobs?q={keywords.replace(' ', '+')}"
            if location:
                search_url += f"&l={location.replace(' ', '+')}"
            
            for page in range(pages):
                page_url = f"{search_url}&start={page * 10}"
                
                if not self.safe_navigate(page_url):
                    continue
                
                # Wait for job listings to load
                job_cards = self.stealth_driver.wait_and_find_element(
                    self.driver, By.CSS_SELECTOR, "[data-testid='job-title']"
                )
                
                if not job_cards:
                    continue
                
                # Find all job cards
                if self.driver is not None:
                    job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
                    
                    for job_elem in job_elements:
                        try:
                            job_data = self.extract_job_data(job_elem)
                            if job_data:
                                jobs.append(job_data)
                        except Exception as e:
                            print(f"Error extracting job data: {e}")
                            continue
                else:
                    print("Driver is not initialized. Skipping job extraction for this page.")
                
                # Random delay between pages
                time.sleep(random.uniform(3, 7))
        
        except Exception as e:
            print(f"Error scraping Indeed: {e}")
        
        finally:
            self.cleanup()
        
        return jobs
    
    def extract_job_data(self, job_element) -> Dict:
        """Extract job data from Indeed job card"""
        try:
            # Title
            try:
                title_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-title'] span")
                title = title_elem.get_attribute("title") or title_elem.text
            except Exception:
                title = ""

            # Company
            try:
                company_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='company-name'] span")
                company = company_elem.get_attribute("title") or company_elem.text
            except Exception:
                company = ""

            # Location
            try:
                location_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-location']")
                location = location_elem.text
            except Exception:
                location = ""

            # Link
            try:
                link_elem = job_element.find_element(By.CSS_SELECTOR, "[data-testid='job-title'] a")
                job_link = link_elem.get_attribute("href")
            except Exception:
                job_link = ""

            # Job ID
            try:
                job_id = job_element.get_attribute("data-jk")
            except Exception:
                job_id = ""

            if not (title and company and job_link):
                return None # type: ignore

            return {
                "id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "link": job_link,
                "source": "Indeed",
                "scraped_at": time.time()
            }

        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None # type: ignore

# Example usage
if __name__ == "__main__":
    scraper = IndeedScraper(headless=False)  # Set to True for production
    jobs = scraper.search_jobs("software engineer", "San Francisco", pages=2)
    
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Link: {job['link']}")
        print("-" * 50)
