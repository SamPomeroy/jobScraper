import uuid
import os
import time
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from bs4.element import Tag

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from supabase import create_client, Client
from crawl4ai import WebCrawler


# === SETUP ===

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in the .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_headless_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")

    driver_path = "C:/Users/snoep_a5dedf8/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    if not os.path.isfile(driver_path):
        raise FileNotFoundError(f"❌ ChromeDriver not found at: {driver_path}")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# === CUSTOM WRAPPER FOR crawl4ai ===

class CustomCrawler:
    def __init__(self):
        browser = get_headless_browser()
        self.crawler = WebCrawler(browser)

    async def get_text(self, url):
        return await self.crawler.get_text(url)


crawler = CustomCrawler()
keyword = "Front End Developer"
url = f"https://www.careerbuilder.com/jobs?keywords={keyword.replace(' ', '+')}&cb_workhome=remote"


def extract_jobs():
    driver = get_headless_browser()
    driver.get(url)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ol#jobs_collection > li.data-results-content-parent"))
        )
        time.sleep(2)  # Allow JS content to finish loading
    except Exception as e:
        print("⚠️ Timed out waiting for job listings to load.")
        with open("careerbuilder_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.quit()
        return []

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    job_cards = soup.select("ol#jobs_collection > li.data-results-content-parent")

    print(f"🔍 Found {len(job_cards)} job listings.")

    jobs = []

    for card in job_cards:
        if not isinstance(card, Tag):
            continue

        title_tag = card.select_one(".data-results-title")
        detail_spans = card.select(".data-details span")
        summary_tag = card.select_one(".data-snapshot .block.show-mobile")
        job_url_tag = card.select_one("a.job-listing-item")

        title = title_tag.text.strip() if title_tag else "Unknown Title"
        company = detail_spans[0].text.strip() if len(detail_spans) > 0 else "Unknown Company"
        location = detail_spans[1].text.strip() if len(detail_spans) > 1 else "Remote"
        job_url = f"https://www.careerbuilder.com{job_url_tag['href']}" if job_url_tag and job_url_tag.get("href") else ""

        if not job_url:
            continue

        # Fetch full description with crawl4ai
        try:
            description = asyncio.run(crawler.get_text(job_url))[:500]
        except Exception as e:
            print(f"⚠️ Failed to get description from {job_url}: {e}")
            description = summary_tag.text.strip()[:500] if summary_tag else "Error fetching description"

        job = {
            "id": str(uuid.uuid4()),
            "title": title,
            "company": company,
            "job_location": location,
            "job_state": "Remote",
            "date": datetime.today().date().isoformat(),
            "site": "CareerBuilder",
            "job_description": description,
            "salary": "N/A",
            "url": job_url,
            "applied": False,
            "search_term": keyword,
            "skills": [],
            "priority": 0,
            "status": "new",
            "inserted_at": datetime.utcnow().isoformat(),
            "last_verified": None,
            "user_id": None
        }

        jobs.append(job)

    return jobs


def upload_to_supabase(jobs):
    for job in jobs:
        supabase.table("jobs").insert(job).execute()


if __name__ == "__main__":
    job_data = extract_jobs()
    if job_data:
        upload_to_supabase(job_data)
        print(f"✅ {len(job_data)} jobs uploaded to Supabase.")
    else:
        print("⚠️ No jobs found or uploaded.")
