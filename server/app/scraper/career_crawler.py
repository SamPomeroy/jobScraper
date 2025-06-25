import sys
import os
import time
import uuid
import random
import csv
import traceback
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from app.db.connect_database import get_db_connection
from app.db.cleanup import cleanup

TECH_KEYWORDS = sys.argv[1].split(",") if len(sys.argv) > 1 else [
  "software engineer", "front-end developer", "back-end developer", "full-stack developer",
  "mobile app developer", "web developer", "wordpress developer", "shopify developer",
  "react developer", "vue.js developer", "angular developer", "javascript developer",
  "typescript developer", "html/css developer", "ui developer", "ux/ui developer",
  "web designer", "interaction designer", "accessibility specialist", "devops engineer",
  "qa engineer", "data analyst", "data scientist", "data engineer", "machine learning engineer",
  "ai developer", "python engineer", "python developer", "python web developer",
  "python data scientist", "python full stack developer", "cloud engineer", "cloud architect",
  "systems administrator", "network engineer", "site reliability engineer", "platform engineer",
  "product manager", "technical product manager", "ux designer", "ui designer",
  "cybersecurity analyst", "security engineer", "information security manager", "it support specialist",
  "help desk technician", "soc analyst", "blockchain developer", "ar/vr developer",
  "robotics engineer", "prompt engineer", "technical program manager", "database administrator",
  "etl developer", "solutions architect", "scrum master", "technical writer",
  "api integration specialist", "web performance engineer", "web accessibility engineer",
  "seo specialist", "web content manager"
]

LOCATION = "remote"
PAGES_PER_KEYWORD = 2
MAX_DAYS = 15

def configure_webdriver():
    opts = uc.ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return uc.Chrome(options=opts)

def insert_job_to_db(job: dict):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO jobs (
                id, title, company, job_location, job_state, date, site,
                job_description, salary, url, applied, search_term, inserted_at
            ) VALUES (
                gen_random_uuid(), %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, NOW()
            )
            ON CONFLICT (url) DO NOTHING
        """, (
            job["title"], job["company"], job["job_location"], job["job_state"],
            job["date"], job["site"], job["job_description"], job["salary"],
            job["url"], job["applied"], job["search_term"]
        ))
        conn.commit()
    except Exception as e:
        print("❌ DB insert error:", e)
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()

def scrape_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD):
    base_url = "https://www.careerbuilder.com"
    driver = configure_webdriver()
    jobs = []
    seen_urls = set()

    try:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 '{keyword}' search at location '{location}'")
            for page in range(1, pages + 1):
                url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"
                driver.get(url)
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "li.data-results-content-parent"))
                    )
                except:
                    print("⚠️ Skipping — no job cards found.")
                    break

                cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")

                for card in cards:
                    try:
                        title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
                        spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
                        company = spans[0].text.strip() if len(spans) > 0 else "N/A"
                        job_location = spans[1].text.strip() if len(spans) > 1 else location
                        job_state = job_location.lower()

                        link = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
                        job_url = link.get_attribute("href") or ""
                        if not job_url or job_url in seen_urls:
                            continue
                        seen_urls.add(job_url)

                        driver.execute_script("window.open(arguments[0])", job_url)
                        driver.switch_to.window(driver.window_handles[-1])
                        try:
                            WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
                            )
                            description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
                        except:
                            description = ""
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                        job = {
                            "title": title,
                            "company": company,
                            "job_location": job_location,
                            "job_state": job_state,
                            "date": datetime.today().date(),
                            "site": "CareerBuilder",
                            "job_description": description,
                            "salary": "N/A",
                            "url": job_url,
                            "applied": False,
                            "search_term": keyword
                        }

                        insert_job_to_db(job)
                        jobs.append(job)

                    except Exception as e:
                        print(f"❌ Error parsing card: {e}")
                        continue
    finally:
        driver.quit()

    return jobs

def write_jobs_csv(jobs: list):
    if not jobs:
        return
    today = datetime.now().strftime("%m-%d-%Y")
    path = os.path.join("data", "career_builder")
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, f"{today}.csv")
    seen = set()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(jobs[0].keys()))
        writer.writeheader()
        for job in jobs:
            if job["url"] not in seen:
                writer.writerow(job)
                seen.add(job["url"])
    print(f"📁 CSV saved to {filename}")

def main():
    print("📡 CareerBuilder Scraper Starting…")
    jobs = scrape_careerbuilder()
    print(f"\n🗂️ Total jobs collected: {len(jobs)}")
    write_jobs_csv(jobs)
    cleanup(MAX_DAYS)

if __name__ == "__main__":
    main()