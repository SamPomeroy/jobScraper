from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from supabase import create_client, Client
import json
import os
from dotenv import load_dotenv
load_dotenv()

# 🛠 Configs
SKILL_FILE = "skills.json"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
TABLE_NAME = "jobs"

# 🎛 Chrome setup
def configure_chrome_options():
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")

    return chrome_options

def insert_jobs_to_supabase(jobs):
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in the environment variables.")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    for job in jobs:
        try:
            response = supabase.table(TABLE_NAME).insert(job).execute()
            if not response.data:
                print(f"Insertion issue: {response}")
        except Exception as e:
            print(f"Exception during Supabase insert: {e}")

def load_skills():
    with open(SKILL_FILE) as f:
        return set(json.load(f))

def extract_skills(text, skills):
    return [skill for skill in skills if skill.lower() in text.lower()]

def get_job_description(driver, url):
    driver.get(url)
    try:
        desc_wait = WebDriverWait(driver, 20)
        desc_container = desc_wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='job_description']"))
        )
        return desc_container.text
    except:
        return "N/A"

def validate_element_text(tag, default="N/A"):
    return tag.get_text(strip=True) if tag else default


def get_job_listings(url, keyword):
    driver_path = "C:/Users/snoep_a5dedf8/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=configure_chrome_options())
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='job_result_two_pane']")))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_cards = soup.select("div[class*='job_result_two_pane']")
    skill_list = load_skills()
    jobs = []

    for card in job_cards:
        try:
            h2_tag = card.select_one("h2")
            title = validate_element_text(h2_tag)
            company_tag = card.select_one("a[data-testid='job-card-company']")
            company = validate_element_text(company_tag)
            location_tag = card.select_one("a[data-testid='job-card-location']")
            location = validate_element_text(location_tag)
            job_state = location.split(",")[-1].strip() if "," in location else location

            a_tag = card.select_one("a")
            if a_tag and a_tag.has_attr("href"):
                job_relative_url = a_tag["href"]
                job_url = f"https://www.ziprecruiter.com{job_relative_url}"
            else:
                print("Warning: No job link found in card, skipping.")
                continue

            full_desc = get_job_description(driver, job_url)
            matched_skills = extract_skills(full_desc, skill_list)

            job = {
                "title": title,
                "company": company,
                "job_location": location,
                "job_state": job_state,
                "date": str(datetime.today().date()),
                "site": "ZipRecruiter",
                "job_description": full_desc,
                "salary": "N/A",
                "url": job_url,
                "applied": False,
                "search_term": keyword,
                "skills": matched_skills,
                "priority": 0,
                "status": "new"
            }

            jobs.append(job)
        except Exception as e:
            print(f"Error parsing job card: {e}")
            continue

    driver.quit()
    return jobs

def main():
    keyword = "Web Developer"
    url = "https://www.ziprecruiter.com/jobs-search?search=Web+Developer&location=remote"
    job_results = get_job_listings(url, keyword)
    insert_jobs_to_supabase(job_results)
    print(f"Inserted {len(job_results)} jobs to Supabase.")
    
if __name__ == "__main__":
    main()
