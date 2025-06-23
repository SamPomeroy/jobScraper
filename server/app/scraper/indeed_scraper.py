import sys
import time
import uuid
import random
import traceback
import pandas as pd
from datetime import datetime
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from db.connect_database import get_db_connection

# ✅ Dynamic keyword input
TECH_KEYWORDS = sys.argv[1].split(",") if len(sys.argv) > 1 else [
  "software engineer",
  "front-end developer",
  "back-end developer",
  "full-stack developer",
  "mobile app developer",
  "web developer",
  "wordpress developer",
  "shopify developer",
  "react developer",
  "vue.js developer",
  "angular developer",
  "javascript developer",
  "typescript developer",
  "html/css developer",
  "ui developer",
  "ux/ui developer",
  "web designer",
  "interaction designer",
  "accessibility specialist",
  "devops engineer",
  "qa engineer",
  "data analyst",
  "data scientist",
  "data engineer",
  "machine learning engineer",
  "ai developer",
  "python engineer",
  "python developer",
  "python web developer",
  "python data scientist",
  "python full stack developer",
  "cloud engineer",
  "cloud architect",
  "systems administrator",
  "network engineer",
  "site reliability engineer",
  "platform engineer",
  "product manager",
  "technical product manager",
  "ux designer",
  "ui designer",
  "cybersecurity analyst",
  "security engineer",
  "information security manager",
  "it support specialist",
  "help desk technician",
  "soc analyst",
  "blockchain developer",
  "ar/vr developer",
  "robotics engineer",
  "prompt engineer",
  "technical program manager",
  "database administrator",
  "etl developer",
  "solutions architect",
  "scrum master",
  "technical writer",
  "api integration specialist",
  "web performance engineer",
  "web accessibility engineer",
  "seo specialist",
  "web content manager"
]
LOCATION = "remote"

def configure_webdriver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36")
    for attempt in range(3):
        try:
            return uc.Chrome(options=options, headless=False)
        except Exception as e:
            print(f"🚧 Driver init failed (attempt {attempt+1}): {e}")
            time.sleep(2)
    raise Exception("Chrome driver could not be initialized after multiple attempts.")

def is_tech_job(title):
    return any(keyword.lower() in title.lower() for keyword in TECH_KEYWORDS)

def parse_date(raw_date):
    if "today" in raw_date.lower() or "just posted" in raw_date.lower():
        return datetime.today().date()
    try:
        num = int(raw_date.strip().split()[0])
        return datetime.today().date() - pd.Timedelta(days=num)
    except:
        return datetime.today().date()

def insert_job_to_db(job):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO jobs (
                id, title, company, job_location, job_state, date, site,
                job_description, salary, url, applied, search_term
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
        """, (
            str(uuid.uuid4()),
            job["title"], job["company"], job["job_location"], job["job_state"],
            job["date"], job["site"], job["job_description"], job["salary"],
            job["url"], job["applied"], job["search_term"]
        ))
        conn.commit()
    except Exception as e:
        print(f"❌ DB insert error: {e}")
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()

def scrape_jobs(location, days=30):
    base_url = "https://www.indeed.com"
    jobs_scraped = []
    driver = None

    try:
        driver = configure_webdriver()
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 Searching '{keyword}' in '{location}'...")
            url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"
            driver.get(url)
            time.sleep(3)

            while True:
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'mainContentTable')]"))
                    )
                except Exception:
                    print("⚠️ Job container did not load.")
                    break

                time.sleep(random.uniform(1.5, 2.5))
                job_cards = driver.find_elements(By.XPATH, "//table[contains(@class, 'mainContentTable')]")
                print(f"🧾 Found {len(job_cards)} job cards.")

                if not job_cards:
                    break

                for table in job_cards:
                    try:
                        if not table.find_elements(By.XPATH, ".//a[@data-jk]"):
                            continue

                        title_el = table.find_element(By.XPATH, ".//h2[contains(@class, 'jobTitle')]/a/span")
                        title = title_el.text.strip()
                        if not is_tech_job(title):
                            continue

                        company_el = table.find_element(By.XPATH, ".//span[@data-testid='company-name']")
                        location_el = table.find_element(By.XPATH, ".//div[@data-testid='text-location']")
                        link_el = table.find_element(By.XPATH, ".//a[@data-jk]")

                        try:
                            date_el = table.find_element(By.XPATH, ".//span[contains(@class, 'date')]")
                            raw_date = date_el.text.strip()
                        except:
                            raw_date = ""
                        date_posted = parse_date(raw_date)

                        jk_value = link_el.get_attribute("data-jk") or ""
                        job_url = base_url + "/viewjob?jk=" + jk_value
                        driver.execute_script("arguments[0].scrollIntoView(true);", table)
                        link_el.click()
                        time.sleep(2)

                        try:
                            desc_el = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
                            )
                            full_description = desc_el.text.strip()
                        except:
                            full_description = "N/A"

                        job = {
                            "title": title,
                            "company": company_el.text.strip() if company_el else "N/A",
                            "job_location": location_el.text.strip() if location_el else location,
                            "job_state": location.lower(),
                            "date": date_posted,
                            "site": "Indeed",
                            "job_description": full_description,
                            "salary": "N/A",
                            "url": job_url,
                            "applied": False,
                            "search_term": keyword
                        }

                        insert_job_to_db(job)
                        jobs_scraped.append(job)

                    except Exception as e:
                        print(f"❌ Error parsing job card: {e}")
                        continue

                try:
                    next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
                    if next_btn.is_enabled():
                        print("➡️ Moving to next page...")
                        driver.execute_script("arguments[0].click();", next_btn)
                        time.sleep(2)
                    else:
                        break
                except:
                    break

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass  

    return jobs_scraped

def main():
    print("📡 Dynamic Tech Job Scraper\n----------------------------")
    all_jobs = scrape_jobs(LOCATION, days=30)
    print(f"\n🗂️ Total jobs collected: {len(all_jobs)}")

    if all_jobs:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"indeed_jobs_{timestamp}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_jobs[0].keys())
            writer.writeheader()
            writer.writerows(all_jobs)
        print(f"📁 Jobs saved to indeed_jobs_{timestamp}.csv")

if __name__ == "__main__":
    main()