import sys
import csv
import time
import uuid
import random
import traceback
import os
from datetime import datetime
from dotenv import load_dotenv
from app.utils.file_helpers import write_jobs_to_csv
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.db.connect_database import get_db_connection

from app.db.cleanup import cleanup
# app/db/supabase_client.py
from supabase import create_client
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables must be set")
supabase = create_client(url, key)


def load_skill_matrix():
    response = supabase.table("skill_categories").select("*").execute()
    return response.data  # list of {'category': ..., 'skills': [...]}

TECH_KEYWORDS = [
    # "software engineer", "front-end developer"
    "back-end developer", "full-stack developer",
#   "mobile app developer", "web developer", "wordpress developer", "shopify developer",
#   "react developer", "vue.js developer", "angular developer", "javascript developer",
#   "typescript developer", "html/css developer", "ui developer", "ux/ui developer",
#   "web designer", "interaction designer", "accessibility specialist", "devops engineer",
#   "qa engineer", "data analyst", "data scientist", "data engineer", "machine learning engineer",
#   "ai developer", "python engineer", "python developer", "python web developer",
#   "python data scientist", "python full stack developer", "cloud engineer", "cloud architect",
#   "systems administrator", "network engineer", "site reliability engineer", "platform engineer",
#   "product manager", "technical product manager", "ux designer", "ui designer",
#   "cybersecurity analyst", "security engineer", "information security manager", "it support specialist",
#   "help desk technician", "soc analyst", "blockchain developer", "ar/vr developer",
#   "robotics engineer", "prompt engineer", "technical program manager", "database administrator",
#   "etl developer", "solutions architect", "scrum master", "technical writer",
#   "api integration specialist", "web performance engineer", "web accessibility engineer",
#   "seo specialist", "web content manager"
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
    finally:
        cur.close()
        conn.close()

def scrape_indeed(location="remote", days=15):
    base_url = "https://www.indeed.com"
    indeed_jobs_scraped = []
    driver = configure_driver()

    try:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 Searching '{keyword}' in '{location}'")
            query = "+".join(keyword.split())
            url = f"{base_url}/jobs?q={query}&l={location}&fromage={days}"

            driver.get(url)
            time.sleep(random.uniform(2, 3))

            if not driver.session_id:
                print("⚠️ Session closed unexpectedly—skipping this keyword")
                continue

            cards = driver.find_elements(By.CSS_SELECTOR, "table.mainContentTable")
            print(f"🧾 Found {len(cards)} job cards")

            for card in cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a span").text.strip()
                    company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
                    job_location = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
                    job_state = job_location.lower()

                    href = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    if not href:
                        continue

                    job_url = href if href.startswith("http") else base_url + href

                    driver.execute_script("window.open(arguments[0]);", job_url)
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)

                    try:
                        WebDriverWait(driver, 7).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#jobDescriptionText"))
                        )
                        full_desc = driver.find_element(By.CSS_SELECTOR, "#jobDescriptionText").text.strip()
                    except:
                        full_desc = ""

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    job = {
                        "title": title,
                        "company": company,
                        "job_location": job_location,
                        "job_state": job_state,
                        "date": datetime.today().date(),
                        "site": "Indeed",
                        "job_description": full_desc or "",
                        "salary": "N/A",
                        "url": job_url,
                        "applied": False,
                        "search_term": keyword
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














# import sys
# import csv
# import time
# import uuid
# import random
# import traceback
# import os
# from datetime import datetime
# from dotenv import load_dotenv

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from app.db.connect_database import get_db_connection
# from app.utils.file_helpers import write_jobs_to_csv
# from app.db.cleanup import cleanup
# load_dotenv()

# TECH_KEYWORDS = [
#     "software engineer","front-end developer"
# ]

# def configure_webdriver():
#     options = uc.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     # options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     # options.add_experimental_option("useAutomationExtension", False)
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.50 Safari/537.36"
#     )

#     driver = uc.Chrome(options=options, headless=False)

#     # 🛡 Add stealth script to bypass navigator.webdriver detection
#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         "source": """
#             Object.defineProperty(navigator, 'webdriver', {
#                 get: () => undefined
#             })
#         """
#     })

#     return driver

# def insert_job_to_db(job: dict):
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             INSERT INTO jobs
#               (id, title, company, job_location, job_state, date, site,
#                job_description, salary, url, applied, search_term)
#             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#             ON CONFLICT (url) DO NOTHING
#         """, (
#             str(uuid.uuid4()), job["title"], job["company"],
#             job["job_location"], job["job_state"],
#             job["date"], job["site"],
#             job["job_description"], job["salary"],
#             job["url"], job["applied"],
#             job["search_term"]
#         ))
#         conn.commit()
#     except Exception as e:
#         print("❌ DB insert error:", e)
#     finally:
#         cur.close()
#         conn.close()

# def scrape_indeed(location="remote", days=15):
#     base_url = "https://www.indeed.com"
#     indeed_jobs_scraped = []
#     driver = configure_webdriver()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             query = "+".join(keyword.split())
#             url = f"{base_url}/jobs?q={query}&l={location}&fromage={days}"

#             driver.get(url)
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
#                         "search_term": keyword
#                     }

#                     indeed_jobs_scraped.append(job)
#                     insert_job_to_db(job)

#                 except Exception as e:
#                     print("❌ Error parsing job card:", e)
#                     traceback.print_exc()
#                     continue

#     finally:
#         driver.quit()
#         if indeed_jobs_scraped:
#             write_jobs_to_csv(indeed_jobs_scraped, prefix="Indeedjobs")
    
#         cleanup(days)

#     return indeed_jobs_scraped








# # import sys
# # import csv
# # import time
# import uuid
# import random
# import traceback
# import os
# from datetime import datetime
# from dotenv import load_dotenv

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from app.db.connect_database import get_db_connection
# from app.utils.file_helpers import write_jobs_to_csv  # 🔁 Make sure this exists

# load_dotenv()

# TECH_KEYWORDS = (
#     # sys.argv[1].split(",") if len(sys.argv) > 1 else [
#         "software engineer",
#         "front-end developer",
#         "back-end developer",
#         "full-stack developer",
#         "mobile app developer",
#         "web developer",
#         "wordpress developer",
#         "shopify developer",
#         "react developer",
#         "vue.js developer",
#         "angular developer",
#         "javascript developer",
#         "typescript developer",
#         "html/css developer",
#         "ui developer",
#         "ux/ui developer",
#         "web designer",
#         "devops engineer",
#         "data analyst",
#         "data scientist",
#         "data engineer",
#         "machine learning engineer",
#         "ai developer",
#         "python developer",
#         "cloud engineer",
#         "systems administrator",
#         "product manager",
#         "technical writer",
#         "cybersecurity analyst"
#     # ]
# )

# LOCATION = "remote"
# def configure_driver():
#     options = uc.ChromeOptions()
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("--start-maximized")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.50 Safari/537.36"
#     )
#     return uc.Chrome(headless="new", options=options)

# def insert_job_to_db(job: dict):
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             INSERT INTO jobs
#               (id, title, company, job_location, job_state, date, site,
#                job_description, salary, url, applied, search_term)
#             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#             ON CONFLICT (url) DO NOTHING
#         """, (
#             str(uuid.uuid4()), job["title"], job["company"],
#             job["job_location"], job["job_state"],
#             job["date"], job["site"],
#             job["job_description"], job["salary"],
#             job["url"], job["applied"],
#             job["search_term"]
#         ))
#         conn.commit()
#     except Exception as e:
#         print("❌ DB insert error:", e)
#     finally:
#         cur.close()
#         conn.close()

# def scrape_indeed(location="remote", days=15):
#     base_url = "https://www.indeed.com"
#     indeed_jobs_scraped = []
#     driver = configure_driver()
    
#     if not driver.session_id:
#         print("⚠️ Session closed unexpectedly—skipping this keyword")
#         break


#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             query = "+".join(keyword.split())
#             url = f"{base_url}/jobs?q={query}&l={location}&fromage={days}"

#             driver.get(url)
#             time.sleep(random.uniform(2, 3))

#             cards = driver.find_elements(By.CSS_SELECTOR, "a.tapItem")
#             print(f"🧾 Found {len(cards)} job cards")

#             for card in cards:
#                 try:
#                     title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text.strip()
#                     company = card.find_element(By.CSS_SELECTOR, ".companyName").text.strip()
#                     job_location = card.find_element(By.CSS_SELECTOR, ".companyLocation").text.strip()
#                     job_state = job_location.lower()

#                     href = card.get_attribute("href")
#                     if not href:
#                         continue 

#                     job_url = href if href.startswith("http") else base_url + href

#                     driver.execute_script("window.open(arguments[0]);", job_url)
#                     driver.switch_to.window(driver.window_handles[-1])
#                     time.sleep(1)

#                     try:
#                         WebDriverWait(driver, 7).until(
#                             EC.presence_of_element_located((By.CSS_SELECTOR, "#jobDescriptionText"))
#                         )
#                         full_desc = driver.find_element(By.CSS_SELECTOR, "#jobDescriptionText").text.strip()
#                     except:
#                         full_desc = ""

#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])

#                     job = {
#                         "title":           title,
#                         "company":         company,
#                         "job_location":    job_location,
#                         "job_state":       job_state,
#                         "date":            datetime.today().date(),
#                         "site":            "Indeed",
#                         "job_description": full_desc or "",
#                         "salary":          "N/A",
#                         "url":             job_url,
#                         "applied":         False,
#                         "search_term":     keyword
#                     }

#                     indeed_jobs_scraped.append(job)
#                     insert_job_to_db(job)

#                 except Exception as e:
#                     print("❌ Error parsing job card:", e)
#                     traceback.print_exc()
#                     continue

#     finally:
#         driver.quit()
#         if indeed_jobs_scraped:
#             write_jobs_to_csv(indeed_jobs_scraped, prefix="Indeedjobs")

#     return indeed_jobs_scraped









# import time
# import random
# from datetime import datetime
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# # Make sure to import or define insert_job_to_db before using it
# # from .db_utils import insert_job_to_db

# from selenium import webdriver

# def configure_webdriver():
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     driver = webdriver.Chrome(options=options)
#     return driver

# def get_jobs_from_crawl4ai(location="remote", days=30):
#     print(f"🌐 Scraping Indeed via Crawl4AI for location='{location}'")
#     base_url = "https://www.indeed.com"
#     jobs_scraped = []
#     driver = configure_webdriver()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'...")
#             url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"
#             driver.get(url)
#             driver.execute_script("window.scrollBy(0, 400);")
#             time.sleep(random.uniform(1.5, 3))

#             while True:
#                 try:
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'mainContentTable')]"))
#                     )
#                 except Exception:
#                     print("⚠️ Job container did not load.")
#                     break

#                 job_cards = driver.find_elements(
#                     By.XPATH, "//ul[contains(@class, 'jobsearch-ResultsList')]/li//table[contains(@class, 'mainContentTable')]"
#                 )
#                 print(f"🧾 Found {len(job_cards)} job cards.")

#                 for table in job_cards:
#                     try:
#                         if not table.find_elements(By.XPATH, ".//a[@data-jk]"):
#                             continue

#                         title_el = table.find_element(By.XPATH, ".//h2[contains(@class, 'jobTitle')]/a/span")
#                         title = title_el.text.strip()
#                         if not is_tech_job(title):
#                             continue

#                         company_el = table.find_element(By.XPATH, ".//span[@data-testid='company-name']")
#                         location_el = table.find_element(By.XPATH, ".//div[@data-testid='text-location']")
#                         link_el = table.find_element(By.XPATH, ".//a[@data-jk]")

#                         try:
#                             date_el = table.find_element(By.XPATH, ".//span[contains(@class, 'date')]")
#                             raw_date = date_el.text.strip()
#                         except:
#                             raw_date = ""
#                         date_posted = parse_date(raw_date)

#                         job_url = base_url + "/viewjob?jk=" + link_el.get_attribute("data-jk")
#                         driver.execute_script("arguments[0].scrollIntoView(true);", table)
#                         link_el.click()
#                         time.sleep(2)

#                         try:
#                             desc_el = WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.ID, "jobDescriptionText"))
#                             )
#                             full_description = desc_el.text.strip()
#                         except:
#                             full_description = "N/A"

#                         job = {
#                             "title": title,
#                             "company": company_el.text.strip() if company_el else "N/A",
#                             "job_location": location_el.text.strip() if location_el else location,
#                             "job_state": location.lower(),
#                             "date": date_posted,
#                             "site": "Indeed",
#                             "job_description": full_description,
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword
#                         }

#                         insert_job_to_db(job)
#                         jobs_scraped.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing job card: {e}")
#                         continue
#                 try:
#                     next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
#                     if next_btn.is_enabled():
#                         print("➡️ Moving to next page...")
#                         driver.execute_script("arguments[0].click();", next_btn)
#                         time.sleep(2)
#                     else:
#                         print("🚫 Next button disabled.")
#                         break
#                 except:
#                     print("ℹ️ No next page.")
#                     break

#     finally:
#         if driver:
#             try:
#                 driver.quit()
#             except Exception:
#                 pass  # Silences WinError 6 from undetected_chromedriver on __del__

#     print(f"\n✅ Crawl4AI finished. Total jobs collected: {len(jobs_scraped)}")
#     return jobs_scraped
