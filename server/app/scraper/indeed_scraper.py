# import sys
# import csv
# import time
# import uuid
# import random
# import traceback
# import os
# import json
# from datetime import datetime
# from dotenv import load_dotenv
# from supabase import create_client

# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.utils.file_helpers import write_jobs_to_csv
# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.services.skills import (
#     load_skill_matrix,
#     extract_skills_by_category
# )

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Load environment variables
# load_dotenv()
# url = os.getenv("SUPABASE_URL")
# key = os.getenv("SUPABASE_ANON_KEY")
# if not url or not key:
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables must be set")
# supabase = create_client(url, key)

# def scrape_indeed(location=LOCATION, days=MAX_DAYS):
#     base_url = "https://www.indeed.com"
#     indeed_jobs_scraped = []
#     skill_matrix = load_skill_matrix()
#     driver = configure_driver()

#     try:
#         for keyword in TECH_KEYWORDS:  # Adjust this if TECH_KEYWORDS is a flat list
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             query = "+".join(keyword.split())
#             url = f"{base_url}/jobs?q={query}&l={location}&fromage={days}"

#             try:
#                 driver.get(url)
#             except Exception as e:
#                 print(f"⚠️ Failed to load page for keyword '{keyword}':", e)
#                 continue

#             time.sleep(random.uniform(2, 3))

#             if not driver.session_id:
#                 print("⚠️ Session closed unexpectedly—skipping this keyword")
#                 continue

#             cards = driver.find_elements(By.CSS_SELECTOR, "table.mainContentTable")
#             print(f"🧾 Found {len(cards)} job cards")

#             for card in cards:
#                 try:
#                     title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a span").text.strip()
#                     company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
#                     job_location = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
#                     job_state = job_location.lower()

#                     href = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
#                     if not href:
#                         continue

#                     job_url = href if href.startswith("http") else base_url + href

#                     # Handle extra tabs
#                     if len(driver.window_handles) > 3:
#                         for handle in driver.window_handles[1:]:
#                             try:
#                                 driver.switch_to.window(handle)
#                                 driver.close()
#                             except:
#                                 continue
#                         driver.switch_to.window(driver.window_handles[0])

#                     driver.execute_script("window.open(arguments[0]);", job_url)
#                     time.sleep(1)
#                     driver.switch_to.window(driver.window_handles[-1])
#                     time.sleep(2)

#                     try:
#                         WebDriverWait(driver, 7).until(
#                             EC.presence_of_element_located((By.CSS_SELECTOR, "#jobDescriptionText"))
#                         )
#                         full_desc = driver.find_element(By.CSS_SELECTOR, "#jobDescriptionText").text.strip()
#                     except:
#                         full_desc = ""

#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])

#                     skills_by_category = extract_skills_by_category(full_desc, skill_matrix)

#                     job = {
#                         "title": title,
#                         "company": company,
#                         "job_location": job_location,
#                         "job_state": job_state,
#                         "date": datetime.today().date(),
#                         "site": "Indeed",
#                         "job_description": full_desc or "",
#                         "salary": "N/A",
#                         "url": job_url,
#                         "applied": False,
#                         "saved": False,
#                         "search_term": keyword,
#                         "skills": skills_by_category,
#                         "priority": 0,
#                         "status": "new",
#                         "category": None,
#                         "inserted_at": datetime.utcnow(),
#                         "last_verified": None,
#                         "user_id": None
#                     }
#                     job["date"] = datetime.today().date()
#                     indeed_jobs_scraped.append(job)
#                     insert_job_to_db(job)

#                 except Exception as e:
#                     print("❌ Error parsing job card:", e)
#                     traceback.print_exc()
#                     continue

#     finally:
#         driver.quit()

#     if indeed_jobs_scraped:
#         write_jobs_to_csv(indeed_jobs_scraped, prefix="Indeedjobs")

#     cleanup(days)
#     return indeed_jobs_scraped


import sys
import csv
import time
import uuid
import random
import traceback
import os
import json
from datetime import datetime
from dotenv import load_dotenv

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.utils.file_helpers import write_jobs_to_csv
from app.db.connect_database import get_db_connection
from app.db.cleanup import cleanup
from supabase import create_client
from app.services.skills import extract_skills
# Load environment variables and connect to Supabase
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables must be set")
supabase = create_client(url, key)

def load_skill_matrix():
    response = supabase.table("skill_categories").select("*").execute()
    return response.data 



def extract_skills(description: str, skill_matrix: list[dict]) -> list[str]:
    skills = []
    lowered_desc = description.lower()
    for row in skill_matrix:
        for skill in row.get("skills", []):
            if skill.lower() in lowered_desc:
                skills.append(skill)
    return list(set(skills))

TECH_KEYWORDS = [
  
    #   "software engineer",
    #   "front-end developer",
      "back-end developer",
      "full-stack developer",
      "mobile app developer",
    #   "web developer",
    #   "wordpress developer",
    #   "shopify developer",
    #   "react developer",
    #   "vue.js developer",
    #   "angular developer",
    #   "javascript developer",
    #   "typescript developer",
    #   "html/css developer",
    #   "ui developer",
    #   "ux/ui developer",
    #   "web designer",
    #   "interaction designer",
    #   "accessibility specialist",
    #   "devops engineer",
    #   "qa engineer",
    #   "data analyst",
    #   "data scientist",
    #   "data engineer",
    #   "machine learning engineer",
    #   "ai developer",
    #   "python engineer",
    #   "python developer",
    #   "python web developer",
    #   "python data scientist",
    #   "python full stack developer",
    #   "cloud engineer",
    #   "cloud architect",
    #   "systems administrator",
    #   "network engineer",
    #   "site reliability engineer",
    #   "platform engineer",
    #   "product manager",
    #   "technical product manager",
    #   "ux designer",
    #   "ui designer",
    #   "cybersecurity analyst",
    #   "security engineer",
    #   "information security manager",
    #   "it support specialist",
    #   "help desk technician",
    #   "soc analyst",
    #   "blockchain developer",
    #   "ar/vr developer",
    #   "robotics engineer",
    #   "prompt engineer",
    #   "technical program manager",
    #   "database administrator",
    #   "etl developer",
    #   "solutions architect",
    #   "scrum master",
    #   "technical writer",
    #   "api integration specialist",
    #   "web performance engineer",
    #   "web accessibility engineer",
    #   "seo specialist",
    #   "web content manager"
    ]


def configure_driver():
    options = uc.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.50 Safari/537.36"
    )

    driver = uc.Chrome(options=options, headless=False)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver

def insert_job_to_db(job: dict):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO jobs (
                id, title, company, job_location, job_state, salary, site,
                date, applied, applied_date, saved, saved_date,
                url, job_description, search_term, category,
                priority, status, status_updated_at, updated_at,
                inserted_at, last_verified, skills
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s
            )
            ON CONFLICT (url) DO NOTHING
        """, (
            str(uuid.uuid4()),
            job["title"], job.get("company"),
            job.get("job_location"), job.get("job_state"), job.get("salary"), job["site"],
            job["date"], job["applied"], job.get("applied_date"), job.get("saved"), job.get("saved_date"),
            job["url"], job.get("job_description"), job.get("search_term"), job.get("category"),
            job.get("priority"), job.get("status"), job.get("status_updated_at"), job.get("updated_at"),
            job.get("inserted_at") or datetime.utcnow().isoformat(), job.get("last_verified"),
            json.dumps(job.get("skills") or [])
        ))
        conn.commit()
    except Exception as e:
        print("❌ DB insert error:", e)
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()

def scrape_indeed(location="remote", days=15):
    base_url = "https://www.indeed.com"
    indeed_jobs_scraped = []
    skill_matrix = load_skill_matrix()
    driver = configure_driver()

    try:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 Searching '{keyword}' in '{location}'")
            query = "+".join(keyword.split())
            url = f"{base_url}/jobs?q={query}&l={location}&fromage={days}"

            try:
                driver.get(url)
            except Exception as e:
                print(f"⚠️ Failed to load page for keyword '{keyword}':", e)
                continue

            time.sleep(random.uniform(2, 4))

            if not driver.session_id:
                print("⚠️ Session closed unexpectedly—skipping this keyword")
                continue

            cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
            print(f"🧾 Found {len(cards)} job cards")

            for card in cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text.strip()
                    company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
                    job_location = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
                    job_state = job_location.lower()

                    link_element = card.find_element(By.CSS_SELECTOR, "a")
                    href = link_element.get_attribute("href")
                    if not href:
                        continue
                    job_url = href if href.startswith("http") else f"{base_url}{href}"

                    # Open in new tab
                    driver.execute_script("window.open(arguments[0]);", job_url)
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)

                    try:
                        WebDriverWait(driver, 7).until(
                            EC.presence_of_element_located((By.ID, "jobDescriptionText"))
                        )
                        full_desc = driver.find_element(By.ID, "jobDescriptionText").text.strip()
                    except:
                        full_desc = ""

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    skills = extract_skills(full_desc, skill_matrix)

                    job = {
                        "title": title,
                        "company": company,
                        "job_location": job_location,
                        "job_state": job_state,
                        "date": datetime.today().date(),
                        "site": "Indeed",
                        "job_description": full_desc,
                        "salary": "N/A",
                        "url": job_url,
                        "applied": False,
                        "search_term": keyword,
                        "skills": skills,
                        "priority": 0,
                        "status": "new"
                    }

                    indeed_jobs_scraped.append(job)
                    insert_job_to_db(job)

                except Exception as e:
                    print("❌ Error parsing job card:", e)
                    traceback.print_exc()
                    continue

    finally:
        driver.quit()
        if indeed_jobs_scraped:
            write_jobs_to_csv(indeed_jobs_scraped, prefix="Indeedjobs")
        cleanup(days)

    return indeed_jobs_scraped
