# import sys
# import os
# import time
# import uuid
# import random
# import csv
# import traceback
# from datetime import datetime, timedelta

# import undetected_chromedriver as uc

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.scraper.career_scraper import TECH_KEYWORDS


# LOCATION = "remote"
# PAGES_PER_KEYWORD = 2
# MAX_DAYS = 15

# def configure_webdriver():
# #     opts = uc.ChromeOptions()
# #     opts.add_argument("--headless")
# #     opts.add_argument("--no-sandbox")
# #     opts.add_argument("--disable-dev-shm-usage")
# #     opts.add_argument(
# #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
# #     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 138.0.7204.50 Safari/537.36"
# # )
# #     return uc.Chrome(options=opts, headless=False)
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

# def parse_date(raw: str):
#     raw = raw.lower()
#     if "today" in raw or "just posted" in raw:
#         return datetime.today().date()
#     try:
#         days_ago = int(raw.strip().split()[0])
#         return datetime.today().date() - timedelta(days=days_ago)
#     except:
#         return datetime.today().date()

# def is_tech_job(title: str) -> bool:
#     return any(keyword.lower() in title.lower() for keyword in TECH_KEYWORDS)


# def insert_job_to_db(job: dict):
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             INSERT INTO jobs (
#                 id, title, company, job_location, job_state, date, site,
#                 job_description, salary, url, applied, search_term, inserted_at
#             ) VALUES (
#                 gen_random_uuid(), %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, NOW()
#             )
#             ON CONFLICT (url) DO NOTHING
#         """, (
#             job["title"], job["company"], job["job_location"], job["job_state"],
#             job["date"], job["site"], job["job_description"], job["salary"],
#             job["url"], job["applied"], job["search_term"]
#         ))
#         conn.commit()
#     except Exception as e:
#         print("❌ DB insert error:", e)
#         traceback.print_exc()
#     finally:
#         cur.close()
#         conn.close()

# def scrape_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=30):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_webdriver()
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 '{keyword}' search at location '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"
#                 driver.get(url)
#                 try:
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_all_elements_located(
#                             (By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except:
#                     print("⚠️ Skipping — no job cards found.")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")

#                 for card in cards:
#                     try:
#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if len(spans) > 0 else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         link = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
#                         job_url = link.get_attribute("href") or ""
#                         if not job_url or job_url in seen_urls:
#                             continue
#                         seen_urls.add(job_url)

#                         # 👀 Before opening the job detail page, clean up old tabs if needed
#                         if len(driver.window_handles) > 3:
#                             for handle in driver.window_handles[1:]:
#                                 try:
#                                     driver.switch_to.window(handle)
#                                     driver.close()
#                                 except:
#                                     continue
#                             driver.switch_to.window(driver.window_handles[0])  # back to main window

#                         # 🪟 Now open the job detail page in a new tab
#                         driver.execute_script("window.open(arguments[0]);", job_url)
#                         time.sleep(1)
#                         driver.switch_to.window(driver.window_handles[-1])
#                         time.sleep(2)

#                         # 📝 Extract the job description
#                         try:
#                             WebDriverWait(driver, 7).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jobDescriptionText"))
#                             )
#                             full_desc = driver.find_element(By.CSS_SELECTOR, "#jobDescriptionText").text.strip()
#                         except:
#                             full_desc = ""

#                         # 🧹 Clean up that tab and return to base
#                         driver.close()
                    
#                         driver.switch_to.window(driver.window_handles[0])
#                         job = {
#                             "title": title,
#                             "company": company,
#                             "job_location": job_location,
#                             "job_state": job_state,
#                             "date": datetime.today().date(),
#                             "site": "CareerBuilder",
#                             "job_description": description,
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword
#                         }

#                         insert_job_to_db(job)
#                         jobs.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing card: {e}")
#                         continue
#     finally:
#         driver.quit()

#     return jobs

# def write_jobs_csv(jobs: list):
#     if not jobs:
#         return
#     today = datetime.now().strftime("%m-%d-%Y")
#     path = os.path.join("data", "career_builder")
#     os.makedirs(path, exist_ok=True)
#     filename = os.path.join(path, f"{today}.csv")
#     seen = set()
#     with open(filename, "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=list(jobs[0].keys()))
#         writer.writeheader()
#         for job in jobs:
#             if job["url"] not in seen:
#                 writer.writerow(job)
#                 seen.add(job["url"])
#     print(f"📁 CSV saved to {filename}")

# def main():
#     print("📡 CareerBuilder Scraper Starting…")
#     jobs = scrape_careerbuilder()
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")
#     write_jobs_csv(jobs)
#     cleanup(MAX_DAYS)

# if __name__ == "__main__":
#     main()



import os
import time
import uuid
import random
import csv
import traceback
from datetime import datetime, timedelta

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

from app.db.connect_database import get_db_connection
from app.db.cleanup import cleanup
from app.services.skills import extract_skills
from app.services.supabase_client import load_skill_matrix
from app.scraper.career_scraper import TECH_KEYWORDS


LOCATION = "remote"
PAGES_PER_KEYWORD = 2
MAX_DAYS = 5


def configure_webdriver():
    options = uc.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment for silent runs
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
                id, title, company, job_location, job_state, date, site,
                job_description, salary, url, applied, search_term, inserted_at, skills
            ) VALUES (
                gen_random_uuid(), %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, NOW(), %s
            )
            ON CONFLICT (url) DO NOTHING
        """, (
            job["title"], job["company"], job["job_location"], job["job_state"],
            job["date"], job["site"], job["job_description"], job["salary"],
            job["url"], job["applied"], job["search_term"], json.dumps(job.get("skills", []))
        ))
        conn.commit()
    except Exception as e:
        print(f"❌ DB insert error: {e}")
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()


def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
    base_url = "https://www.careerbuilder.com"
    driver = configure_webdriver()
    skill_matrix = load_skill_matrix()
    jobs = []
    seen_urls = set()

    try:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 Searching '{keyword}' in '{location}'")
            for page in range(1, pages + 1):
                url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

                try:
                    driver.get(url)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
                    )
                except Exception as e:
                    print(f"⚠️ Skipping — no job cards found on page {page} for '{keyword}': {e}")
                    break

                cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
                for card in cards:
                    try:
                        title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
                        spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
                        company = spans[0].text.strip() if spans else "N/A"
                        job_location = spans[1].text.strip() if len(spans) > 1 else location
                        job_state = job_location.lower()

                        href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
                        if not href or href in seen_urls:
                            continue

                        seen_urls.add(href)
                        job_url = href if href.startswith("http") else base_url + href

                        # 🔁 Tab cleanup: avoid driver crash
                        if len(driver.window_handles) > 3:
                            for handle in driver.window_handles[1:]:
                                try:
                                    driver.switch_to.window(handle)
                                    driver.close()
                                except:
                                    continue
                            driver.switch_to.window(driver.window_handles[0])

                        driver.execute_script("window.open(arguments[0])", job_url)
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(2)

                        try:
                            WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
                            )
                            description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
                        except:
                            description = ""

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                        skills = extract_skills(description, skill_matrix)

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
                            "search_term": keyword,
                            "skills": skills
                        }

                        insert_job_to_db(job)
                        jobs.append(job)

                    except Exception as e:
                        print(f"❌ Error parsing card: {e}")
                        traceback.print_exc()
                        continue
    finally:
        driver.quit()
        return jobs


def write_jobs_csv(jobs: list):
    if not jobs:
        return
    from pathlib import Path
    path = Path("data/career_crawler")
    path.mkdir(parents=True, exist_ok=True)
    filename = path / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(jobs[0].keys()))
        writer.writeheader()
        writer.writerows(jobs)

    print(f"📁 CSV saved to {filename}")


def main():
    print("📡 CareerBuilder Crawler Starting…")
    jobs = get_jobs_from_careerbuilder()
    print(f"\n🗂️ Total jobs collected: {len(jobs)}")
    write_jobs_csv(jobs)
    cleanup(MAX_DAYS)


if __name__ == "__main__":
    main()