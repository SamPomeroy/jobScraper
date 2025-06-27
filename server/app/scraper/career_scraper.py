# import sys
# import time
# import uuid
# import random
# import traceback
# import csv
# import os
# import json
# from dotenv import load_dotenv

# from app.utils.file_helpers import write_jobs_to_csv
# from datetime import datetime
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver as uc
# from app.db.cleanup import cleanup
# from app.db.connect_database import get_db_connection
# from supabase import create_client
# load_dotenv()
# url = os.getenv("SUPABASE_URL")
# key = os.getenv("SUPABASE_ANON_KEY")
# if not url or not key:
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables must be set")
# supabase = create_client(url, key)

# def load_skill_matrix():
#     response = supabase.table("skill_categories").select("*").execute()
#     return response.data  # list of {'category': ..., 'skills': [...]}


# # ✅ Keywords come from CLI or default list
# TECH_KEYWORDS = [
#     sys.argv[1].split(",") if len(sys.argv) > 1 else [
#       "software engineer",
#       "front-end developer",
#       "back-end developer",
#       "full-stack developer",
#       "mobile app developer",
#       "web developer",
#       "wordpress developer",
#       "shopify developer",
#       "react developer",
#       "vue.js developer",
#       "angular developer",
#       "javascript developer",
#       "typescript developer",
#       "html/css developer",
#       "ui developer",
#       "ux/ui developer",
#       "web designer",
#       "interaction designer",
#       "accessibility specialist",
#       "devops engineer",
#       "qa engineer",
#       "data analyst",
#       "data scientist",
#       "data engineer",
#       "machine learning engineer",
#       "ai developer",
#       "python engineer",
#       "python developer",
#       "python web developer",
#       "python data scientist",
#       "python full stack developer",
#       "cloud engineer",
#       "cloud architect",
#       "systems administrator",
#       "network engineer",
#       "site reliability engineer",
#       "platform engineer",
#       "product manager",
#       "technical product manager",
#       "ux designer",
#       "ui designer",
#       "cybersecurity analyst",
#       "security engineer",
#       "information security manager",
#       "it support specialist",
#       "help desk technician",
#       "soc analyst",
#       "blockchain developer",
#       "ar/vr developer",
#       "robotics engineer",
#       "prompt engineer",
#       "technical program manager",
#       "database administrator",
#       "etl developer",
#       "solutions architect",
#       "scrum master",
#       "technical writer",
#       "api integration specialist",
#       "web performance engineer",
#       "web accessibility engineer",
#       "seo specialist",
#       "web content manager"
#     ]
# ]

# # Number of pages to scrape per keyword
# PAGES_PER_KEYWORD = 20


# def configure_driver():
#     options = uc.ChromeOptions()
#     # options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.50 Safari/537.36"
#     )

#     driver = uc.Chrome(options=options, headless=False)

#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         "source": """
#             Object.defineProperty(navigator, 'webdriver', {
#                 get: () => undefined
#             })
#         """
#     })
#     return driver
   
#     # for i in range(3):
#     #     try:
#     #         return uc.Chrome(options=opts, headless=False)
#     #     except Exception as e:
#     #         print(f"🚧 Driver init failed (attempt {i+1}): {e}")
#     #         time.sleep(2)
#     # raise RuntimeError("Chrome driver failed to start after 3 attempts")

# def insert_job_to_db(job: dict):
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             INSERT INTO jobs (
#                 id, title, company, job_location, job_state, salary, site,
#                 date, applied, applied_date, saved, saved_date,
#                 url, job_description, search_term, category,
#                 priority, status, status_updated_at, updated_at,
#                 inserted_at, last_verified, skills
#             ) VALUES (
#                 %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s,
#                 %s, %s, %s, %s,
#                 %s, %s, %s
#             )
#             ON CONFLICT (url) DO NOTHING
#         """, (
#             str(uuid.uuid4()),
#             job["title"], job.get("company"),
#             job.get("job_location"), job.get("job_state"), job.get("salary"), job["site"],
#             job["date"], job["applied"], job.get("applied_date"), job.get("saved"), job.get("saved_date"),
#             job["url"], job.get("job_description"), job.get("search_term"), job.get("category"),
#             job.get("priority"), job.get("status"), job.get("status_updated_at"), job.get("updated_at"),
#             job.get("inserted_at") or datetime.utcnow().isoformat(), job.get("last_verified"),
#             json.dumps(job.get("skills") or [])
#         ))
#         conn.commit()
#     except Exception as e:
#         print("❌ DB insert error:", e)
#         traceback.print_exc()
#     finally:
#         cur.close()
#         conn.close()

# def scrape_careerbuilder(location: str, pages: int = PAGES_PER_KEYWORD, days=30):
#     base_url = "https://www.careerbuilder.com"
#     # query = "+".join(keyword.split())
#     career_jobs_scraped = []
#     driver = configure_driver()
#     results = []

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#         for page in range(1, pages + 1):
#             search_url = (
#                 f"{base_url}/jobs?"
#                 f"keywords={'+'.join(keyword.split())}&"
#                 f"location={location}&"
#                 f"page_number={page}"
#             )
#             try:
#                 driver.get(search_url)
#                 WebDriverWait(driver, 15).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                 )
#             except Exception as e:
#                 print(f"⚠️ Failed to load page or locate job cards for '{keyword}', page {page}: {e}")
#                 break  # or continue if you want to skip page and keep keyword


#             time.sleep(random.uniform(1.0, 2.0))
#             cards = driver.find_elements(
#                 By.CSS_SELECTOR, "li.data-results-content-parent"
#             )
#             print(f"🧾 Found {len(cards)} cards (page {page})")

#             for card in cards:
#                 try:
#                     # Title
#                     title = card.find_element(
#                         By.CSS_SELECTOR, ".data-results-title"
#                     ).text.strip()

#                     # Company / Location
#                     details = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                     company = details[0].text.strip() if details else "N/A"
#                     job_location = details[1].text.strip() if len(details) > 1 else location
#                     job_state = job_location.lower()

#                     # Open detail page in new tab for full description
#                     link_el = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
#                     href = link_el.get_attribute("href") or ""
#                     if not href:
#                         continue
#                     job_url = href if href.startswith("http") else base_url + href

#                    # 👀 Before opening the job detail page, clean up old tabs if needed
#                     if len(driver.window_handles) > 3:
#                         for handle in driver.window_handles[1:]:
#                             try:
#                                 driver.switch_to.window(handle)
#                                 driver.close()
#                             except:
#                                 continue
#                         driver.switch_to.window(driver.window_handles[0])  # back to main window

#                     # 🪟 Now open the job detail page in a new tab
#                     driver.execute_script("window.open(arguments[0]);", job_url)
#                     time.sleep(1)
#                     driver.switch_to.window(driver.window_handles[-1])
#                     time.sleep(2)

#                     # 📝 Extract the job description
#                     try:
#                         WebDriverWait(driver, 7).until(
#                             EC.presence_of_element_located((By.CSS_SELECTOR, "#jobDescriptionText"))
#                         )
#                         full_desc = driver.find_element(By.CSS_SELECTOR, "#jobDescriptionText").text.strip()
#                     except:
#                         full_desc = ""

#                     # 🧹 Clean up that tab and return to base
#                     driver.close()
                   
#                     driver.switch_to.window(driver.window_handles[0])
#                     job = {
#                         "title":           title,
#                         "company":         company,
#                         "job_location":    job_location,
#                         "job_state":       job_state,
#                         "date":            datetime.today().date(),
#                         "site":            "CareerBuilder",
#                         "job_description": full_desc or "",
#                         "salary":          "N/A",
#                         "url":             job_url,
#                         "applied":         False,
#                         "search_term":     keyword
#                     }

#                     career_jobs_scraped.append(job)
#                     insert_job_to_db(job)

#                 except Exception as e:
#                     print("❌ Error parsing card:", e)
#                     traceback.print_exc()
#                     continue

#     finally:
#         driver.quit()
#         if career_jobs_scraped:
#             write_jobs_to_csv(career_jobs_scraped, prefix="careerbuilderjobs")
#         cleanup(days)
#     return career_jobs_scraped
# # def main():
# #     print("📡 CareerBuilder Scraper Starting…")
# #     jobs = scrape_careerbuilder(LOCATION)
# #     print(f"\n🗂️ Total jobs collected: {len(jobs)}")

# #     if jobs:
# #         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
# #         with open(f"careerbuilder_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
# #             writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
# #             writer.writeheader()
# #             writer.writerows(jobs)
# #         print(f"📁 Jobs saved to careerbuilder_jobs_{ts}.csv")

# # if __name__ == "__main__":
# #     main()

import sys
import time
import uuid
import json
import random
import traceback
import os
from datetime import datetime
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from app.utils.file_helpers import write_jobs_to_csv
from app.db.cleanup import cleanup
from app.db.connect_database import get_db_connection
from app.services.skills import extract_skills  # ← Make sure this is present
from app.services.supabase_client import load_skill_matrix

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

# ✅ List of string keywords
TECH_KEYWORDS = [
#     sys.argv[1].split(",") if len(sys.argv) > 1 else [
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
# ]
PAGES_PER_KEYWORD = 2


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


def scrape_careerbuilder(location: str, pages: int = PAGES_PER_KEYWORD, days=30):
    base_url = "https://www.careerbuilder.com"
    driver = configure_driver()
    skill_matrix = load_skill_matrix()
    career_jobs_scraped = []

    try:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 Searching '{keyword}' in '{location}'")
            for page in range(1, pages + 1):
                search_url = (
                    f"{base_url}/jobs?"
                    f"keywords={'+'.join(keyword.split())}&"
                    f"location={location}&"
                    f"page_number={page}"
                )
                try:
                    driver.get(search_url)
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
                    )
                except Exception as e:
                    print(f"⚠️ Failed to load page or locate cards for '{keyword}', page {page}: {e}")
                    break

                time.sleep(random.uniform(1.0, 2.0))
                cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
                print(f"🧾 Found {len(cards)} cards (page {page})")

                for card in cards:
                    try:
                        title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
                        spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
                        company = spans[0].text.strip() if spans else "N/A"
                        job_location = spans[1].text.strip() if len(spans) > 1 else location
                        job_state = job_location.lower()

                        link = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
                        href = link.get_attribute("href") or ""
                        if not href:
                            continue
                        job_url = href if href.startswith("http") else base_url + href

                        # Tab overflow management
                        if len(driver.window_handles) > 3:
                            for h in driver.window_handles[1:]:
                                try:
                                    driver.switch_to.window(h)
                                    driver.close()
                                except:
                                    pass
                            driver.switch_to.window(driver.window_handles[0])

                        driver.execute_script("window.open(arguments[0])", job_url)
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(2)

                        try:
                            WebDriverWait(driver, 7).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
                            )
                            description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
                        except:
                            description = ""

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                        skills = extract_skills(description, skill_matrix)

                        job = {
                            "title":           title,
                            "company":         company,
                            "job_location":    job_location,
                            "job_state":       job_state,
                            "date":            datetime.today().date(),
                            "site":            "CareerBuilder",
                            "job_description": description,
                            "salary":          "N/A",
                            "url":             job_url,
                            "applied":         False,
                            "search_term":     keyword,
                            "skills":          skills,
                            "priority":        0,
                            "status":          "new"
                        }

                        career_jobs_scraped.append(job)
                        insert_job_to_db(job)

                    except Exception as e:
                        print("❌ Error parsing card:", e)
                        traceback.print_exc()
                        continue

    finally:
        driver.quit()
        if career_jobs_scraped:
            write_jobs_to_csv(career_jobs_scraped, prefix="careerbuilderjobs")
        cleanup(days)

    return career_jobs_scraped