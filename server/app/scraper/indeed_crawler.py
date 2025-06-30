# import sys, os, time, csv, json, traceback
# from datetime import datetime

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from dotenv import load_dotenv

# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.utils.common import TECH_KEYWORDS

# LOCATION = "remote"
# MAX_DAYS = 5

# def configure_webdriver():
#     options = uc.ChromeOptions()
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.50 Safari/537.36"
#     )
#     driver = uc.Chrome(options=options, headless=False)
#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
#     })
#     return driver

# def insert_job_to_db(job):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO jobs (
#                 id, title, company, job_location, job_state, date, site,
#                 job_description, salary, url, applied, search_term,
#                 skills, skills_by_category, inserted_at
#             ) VALUES (
#                 gen_random_uuid(), %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s,
#                 %s, %s, NOW()
#             )
#             ON CONFLICT (url) DO NOTHING;
#         """, (
#             job["title"], job["company"], job["job_location"], job["job_state"],
#             job["date"], job["site"], job["job_description"], job["salary"],
#             job["url"], job["applied"], job["search_term"],
#             json.dumps(job["flat_skills"]),  # filled later
#             json.dumps(job["skills_by_category"])  # filled later
#         ))
#         conn.commit()
#     except Exception as e:
#         print(f"❌ DB insert error: {e}")
#         traceback.print_exc()
#     finally:
#         cur.close()
#         conn.close()

# def get_jobs_from_crawl4ai(location=LOCATION, days=MAX_DAYS):
#     print(f"\n🌐 Crawl4AI (Indeed) → {location} (last {days} days)")
#     base_url = "https://www.indeed.com"
#     driver = configure_webdriver()
#     jobs_scraped = []

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching for '{keyword}'")
#             url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"

#             try:
#                 driver.get(url)
#                 time.sleep(2)
#             except Exception as e:
#                 print(f"🚫 Failed to load job search page: {e}")
#                 continue

#             while True:
#                 try:
#                     WebDriverWait(driver, 12).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
#                     )
#                 except:
#                     print("⚠️ Job listings didn’t load.")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
#                 print(f"📄 Found {len(cards)} job cards")

#                 for i in range(len(cards)):
#                     try:
#                         cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
#                         if i >= len(cards):
#                             break
#                         card = cards[i]

#                         title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text.strip()
#                         company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
#                         location_text = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
#                         job_state = location_text.lower()
#                         href = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href") or ""
#                         job_url = href if href.startswith("http") else f"{base_url}{href}"

#                         driver.execute_script("window.open(arguments[0], '_self');", job_url)
#                         time.sleep(2)

#                         try:
#                             WebDriverWait(driver, 7).until(
#                                 EC.presence_of_element_located((By.ID, "jobDescriptionText"))
#                             )
#                             description = driver.find_element(By.ID, "jobDescriptionText").text.strip()
#                         except:
#                             description = "N/A"

#                         job = {
#                             "title": title,
#                             "company": company,
#                             "job_location": location_text,
#                             "job_state": job_state,
#                             "date": datetime.today().date(),
#                             "site": "Indeed",
#                             "job_description": description,
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword,
#                             "flat_skills": [],  # to be filled later
#                             "skills_by_category": {},  # to be filled later
#                         }

#                         insert_job_to_db(job)
#                         jobs_scraped.append(job)

#                         driver.execute_script("window.history.go(-1)")
#                         time.sleep(2)

#                     except Exception as e:
#                         print(f"❌ Error on job scrape: {e}")
#                         traceback.print_exc()
#                         try:
#                             driver.execute_script("window.history.go(-1)")
#                             time.sleep(2)
#                         except:
#                             pass
#                         continue

#                 try:
#                     next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
#                     if next_btn.is_enabled():
#                         driver.execute_script("arguments[0].click();", next_btn)
#                         time.sleep(2)
#                     else:
#                         break
#                 except:
#                     break

#     finally:
#         try: driver.quit()
#         except: pass

#     if jobs_scraped:
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         with open(f"crawl4ai_indeed_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=list(jobs_scraped[0].keys()))
#             writer.writeheader()
#             writer.writerows(jobs_scraped)
#         print(f"📁 Saved to crawl4ai_indeed_jobs_{ts}.csv")

#     cleanup(days)
#     print(f"\n✅ Crawl4AI (Indeed) collected {len(jobs_scraped)} jobs.")
#     return jobs_scraped

# if __name__ == "__main__":
#     jobs = get_jobs_from_crawl4ai()
#     print(f"🎯 Finished scraping. {len(jobs)} jobs returned.")


import sys, os, time, csv, json, traceback
from datetime import datetime, timedelta

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

from app.services.skills_loader import load_all_skills
from app.services.skills import extract_skills_by_category, extract_skills
from app.utils.skill_utils import extract_flat_skills

from app.db.connect_database import get_db_connection
from app.db.cleanup import cleanup
from app.scraper.indeed_scraper import TECH_KEYWORDS

LOCATION = "remote"
MAX_DAYS = 5
SKILLS = load_all_skills()

def configure_webdriver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.50 Safari/537.36")
    driver = uc.Chrome(options=options, headless=False)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def insert_job_to_db(job):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO jobs (
                id, title, company, job_location, job_state, date, site,
                job_description, salary, url, applied, search_term,
                skills, skills_by_category, inserted_at
            ) VALUES (
                gen_random_uuid(), %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, NOW()
            )
            ON CONFLICT (url) DO NOTHING;
        """, (
            job["title"], job["company"], job["job_location"], job["job_state"],
            job["date"], job["site"], job["job_description"], job["salary"],
            job["url"], job["applied"], job["search_term"],
            json.dumps(job["flat_skills"]),  # save as JSON
            json.dumps(job["skills_by_category"])  # categorized
        ))
        conn.commit()
    except Exception as e:
        print(f"❌ DB insert error: {e}")
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()

def get_jobs_from_crawl4ai(location=LOCATION, days=MAX_DAYS):
    print(f"\n🌐 Crawl4AI (Indeed) → {location} (last {days} days)")
    base_url = "https://www.indeed.com"
    driver = configure_webdriver()
    jobs_scraped = []

    try:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 Searching for '{keyword}'")
            url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"

            try:
                driver.get(url)
                time.sleep(2)
            except Exception as e:
                print(f"🚫 Failed to load job search page: {e}")
                continue

            while True:
                try:
                    WebDriverWait(driver, 12).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
                    )
                except:
                    print("⚠️ Job listings didn’t load.")
                    break

                cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
                print(f"📄 Found {len(cards)} job cards")

                for i in range(len(cards)):
                    try:
                        cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
                        if i >= len(cards):
                            break
                        card = cards[i]

                        title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text.strip()
                        company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
                        location_text = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
                        job_state = location_text.lower()
                        href = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href") or ""
                        job_url = href if href.startswith("http") else f"{base_url}{href}"

                        driver.execute_script("window.open(arguments[0], '_self');", job_url)
                        time.sleep(2)

                        try:
                            WebDriverWait(driver, 7).until(
                                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
                            )
                            description = driver.find_element(By.ID, "jobDescriptionText").text.strip()
                        except:
                            description = "N/A"

                        flat_skills = extract_flat_skills(description, SKILLS["flat"])
                        categorized_skills = extract_skills_by_category(description, SKILLS["matrix"])

                        job = {
                            "title": title,
                            "company": company,
                            "job_location": location_text,
                            "job_state": job_state,
                            "date": datetime.today().date(),
                            "site": "Indeed",
                            "job_description": description,
                            "salary": "N/A",
                            "url": job_url,
                            "applied": False,
                            "search_term": keyword,
                            "flat_skills": flat_skills,
                            "skills_by_category": categorized_skills,
                        }

                        insert_job_to_db(job)
                        jobs_scraped.append(job)

                        driver.execute_script("window.history.go(-1)")
                        time.sleep(2)

                    except Exception as e:
                        print(f"❌ Error on job scrape: {e}")
                        traceback.print_exc()
                        try:
                            driver.execute_script("window.history.go(-1)")
                            time.sleep(2)
                        except:
                            pass
                        continue

                try:
                    next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
                    if next_btn.is_enabled():
                        driver.execute_script("arguments[0].click();", next_btn)
                        time.sleep(2)
                    else:
                        break
                except:
                    break

    finally:
        try: driver.quit()
        except: pass

    if jobs_scraped:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"crawl4ai_indeed_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(jobs_scraped[0].keys()))
            writer.writeheader()
            writer.writerows(jobs_scraped)
        print(f"📁 Saved to crawl4ai_indeed_jobs_{ts}.csv")

    cleanup(days)
    print(f"\n✅ Crawl4AI (Indeed) collected {len(jobs_scraped)} jobs.")
    return jobs_scraped

if __name__ == "__main__":
    jobs = get_jobs_from_crawl4ai()
    print(f"🎯 Finished scraping. {len(jobs)} jobs returned.")

# import sys, time, csv, json, traceback
# from datetime import datetime, timedelta

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from app.services.skills import extract_skills, load_skill_matrix
# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.scraper.indeed_scraper import TECH_KEYWORDS

# LOCATION = "remote"
# MAX_DAYS = 5
# skill_matrix = load_skill_matrix()


# def configure_webdriver():
#     options = uc.ChromeOptions()
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.50 Safari/537.36"
#     )
#     driver = uc.Chrome(options=options, headless=False)
#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
#     })
#     return driver


# def insert_job_to_db(job):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO jobs (
#                 id, title, company, job_location, job_state, date, site,
#                 job_description, salary, url, applied, search_term, skills, inserted_at
#             ) VALUES (
#                 gen_random_uuid(), %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, %s, NOW()
#             )
#             ON CONFLICT (url) DO NOTHING;
#         """, (
#             job["title"], job["company"], job["job_location"], job["job_state"],
#             job["date"], job["site"], job["job_description"], job["salary"],
#             job["url"], job["applied"], job["search_term"],
#             json.dumps(job["skills"])  # ⬅️ cast to JSON
#         ))
#         conn.commit()
#     except Exception as e:
#         print(f"❌ DB insert error: {e}")
#         traceback.print_exc()
#     finally:
#         cur.close()
#         conn.close()


# def get_jobs_from_crawl4ai(location=LOCATION, days=MAX_DAYS):
#     print(f"\n🌐 Crawl4AI (Indeed) → {location} (last {days} days)")
#     base_url = "https://www.indeed.com"
#     driver = configure_webdriver()
#     jobs_scraped = []

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching for '{keyword}'")
#             url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"

#             try:
#                 driver.get(url)
#                 time.sleep(2)
#             except Exception as e:
#                 print(f"🚫 Failed to load job search page: {e}")
#                 continue

#             while True:
#                 try:
#                     WebDriverWait(driver, 12).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
#                     )
#                 except:
#                     print("⚠️ Job listings didn’t load.")
#                     break

#                 # ⬇️ Always re-fetch job cards to prevent stale references
#                 card_elements = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
#                 print(f"📄 Found {len(card_elements)} job cards")

#                 for i in range(len(card_elements)):
#                     try:
#                         # 🧼 Re-fetch the card element on each loop
#                         cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
#                         if i >= len(cards):
#                             break
#                         card = cards[i]

#                         title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text.strip()
#                         company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
#                         location_text = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
#                         job_state = location_text.lower()
#                         href = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href") or ""
#                         job_url = href if href.startswith("http") else f"{base_url}{href}"

#                         # Navigate to job page (same tab)
#                         driver.execute_script("window.open(arguments[0], '_self');", job_url)
#                         time.sleep(2)

#                         try:
#                             WebDriverWait(driver, 7).until(
#                                 EC.presence_of_element_located((By.ID, "jobDescriptionText"))
#                             )
#                             description = driver.find_element(By.ID, "jobDescriptionText").text.strip()
#                         except:
#                             description = "N/A"

#                         skills = extract_skills(description, skill_matrix)

#                         job = {
#                             "title": title,
#                             "company": company,
#                             "job_location": location_text,
#                             "job_state": job_state,
#                             "date": datetime.today().date(),
#                             "site": "Indeed",
#                             "job_description": description,
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword,
#                             "skills": skills,
#                         }

#                         insert_job_to_db(job)
#                         jobs_scraped.append(job)

#                         # Return to search results
#                         driver.execute_script("window.history.go(-1)")
#                         time.sleep(2)

#                     except Exception as e:
#                         print(f"❌ Error on job scrape: {e}")
#                         traceback.print_exc()
#                         try:
#                             driver.execute_script("window.history.go(-1)")
#                             time.sleep(2)
#                         except:
#                             pass
#                         continue

#                 try:
#                     next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
#                     if next_btn.is_enabled():
#                         driver.execute_script("arguments[0].click();", next_btn)
#                         time.sleep(2)
#                     else:
#                         break
#                 except:
#                     break

#     finally:
#         try:
#             driver.quit()
#         except:
#             pass

#     if jobs_scraped:
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         with open(f"crawl4ai_indeed_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=list(jobs_scraped[0].keys()))
#             writer.writeheader()
#             writer.writerows(jobs_scraped)
#         print(f"📁 Saved to crawl4ai_indeed_jobs_{ts}.csv")

#     cleanup(days)
#     print(f"\n✅ Crawl4AI (Indeed) collected {len(jobs_scraped)} jobs.")
#     return jobs_scraped


# if __name__ == "__main__":
#     jobs = get_jobs_from_crawl4ai()
#     print(f"🎯 Finished scraping. {len(jobs)} jobs returned.")



# import sys
# import time
# import random
# import csv
# import traceback
# from datetime import datetime, timedelta
# import json
# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from app.services.skills import extract_skills, load_skill_matrix
# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.scraper.indeed_scraper import TECH_KEYWORDS

# LOCATION = "remote"
# MAX_DAYS = 5
# skill_matrix = load_skill_matrix()


# def configure_webdriver():
#     options = uc.ChromeOptions()
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
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO jobs (
#                 id, title, company, job_location, job_state, date, site,
#                 job_description, salary, url, applied, search_term, skills, inserted_at
#             ) VALUES (
#                 gen_random_uuid(), %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, %s, NOW()
#             )
#             ON CONFLICT (url) DO NOTHING;
#         """, (
#             job["title"], job["company"], job["job_location"], job["job_state"],
#             job["date"], job["site"], job["job_description"], job["salary"],
#             job["url"], job["applied"], job["search_term"], json.dumps(job["skills"])

#         ))
#         conn.commit()
#     except Exception as e:
#         print(f"❌ DB insert error: {e}")
#         traceback.print_exc()
#     finally:
#         cur.close()
#         conn.close()

# def get_jobs_from_crawl4ai(location=LOCATION, days=MAX_DAYS):
#     print(f"🌐 Crawl4AI (Indeed) → {location} (last {days} days)")
#     base_url = "https://www.indeed.com"
#     driver = configure_webdriver()
#     jobs_scraped = []
#     skill_matrix = load_skill_matrix()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 '{keyword}'")
#             url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"

#             try:
#                 driver.get(url)
#                 with open(f"debug_{keyword.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
#                     f.write(driver.page_source)
#                 time.sleep(2)
#             except Exception as e:
#                 print(f"🚫 Failed to load search page: {e}")
#                 continue

#             while True:
#                 try:
#                     WebDriverWait(driver, 12).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
#                     )
#                 except:
#                     print("⚠️ Job listings didn’t load.")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
#                 print(f"📄 Found {len(cards)} job cards")

#                 for card in cards:
#                     try:
#                         title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text.strip()
#                         if not is_tech_job(title):
#                             continue

#                         company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
#                         location_text = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
#                         job_state = location_text.lower()

#                         href = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href") or ""
#                         job_url = href if href.startswith("http") else f"{base_url}{href}"

#                         # Visit job page in same tab
#                         driver.execute_script("window.open(arguments[0], '_self');", job_url)
#                         time.sleep(2)

#                         try:
#                             WebDriverWait(driver, 7).until(
#                                 EC.presence_of_element_located((By.ID, "jobDescriptionText"))
#                             )
#                             description = driver.find_element(By.ID, "jobDescriptionText").text.strip()
#                         except:
#                             description = "N/A"

#                         skills = extract_skills(description, skill_matrix)

#                         job = {
#                             "title": title,
#                             "company": company,
#                             "job_location": location_text,
#                             "job_state": job_state,
#                             "date": datetime.today().date(),
#                             "site": "Indeed",
#                             "job_description": description,
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword,
#                             "skills": skills,
#                         }

#                         insert_job_to_db(job)
#                         jobs_scraped.append(job)

#                         # Go back to previous search results
#                         driver.execute_script("window.history.go(-1)")
#                         time.sleep(2)

#                     except Exception as e:
#                         print(f"❌ Error on job scrape: {e}")
#                         traceback.print_exc()
#                         try:
#                             driver.execute_script("window.history.go(-1)")
#                             time.sleep(2)
#                         except:
#                             pass
#                         continue

#                 # Pagination
#                 try:
#                     next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
#                     if next_btn.is_enabled():
#                         driver.execute_script("arguments[0].click();", next_btn)
#                         time.sleep(2)
#                     else:
#                         break
#                 except:
#                     break

#     finally:
#         try: driver.quit()
#         except: pass

#     if jobs_scraped:
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         with open(f"crawl4ai_indeed_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=list(jobs_scraped[0].keys()))
#             writer.writeheader()
#             writer.writerows(jobs_scraped)
#         print(f"📁 Saved to crawl4ai_indeed_jobs_{ts}.csv")

#     cleanup(days)
#     print(f"\n✅ Crawl4AI (Indeed) collected {len(jobs_scraped)} jobs.")
#     return jobs_scraped
# def get_jobs_from_crawl4ai(location=LOCATION, days=MAX_DAYS):
#     print(f"🌐 Crawl4AI (Indeed) → {location} (last {days} days)")
#     base_url = "https://www.indeed.com"
#     driver = configure_webdriver()
#     jobs_scraped = []

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 '{keyword}'")
#             url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"

#             if not driver.session_id:
#                 print("💥 Driver session expired. Restarting...")
#                 try: driver.quit()
#                 except: pass
#                 driver = configure_webdriver()

#             try:
#                 driver.get(url)
#                 with open(f"debug_{keyword.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
#                     f.write(driver.page_source)
#                     print(f"📝 Saved HTML snapshot for '{keyword}'")
#                 time.sleep(2)
#             except Exception as e:
#                 print(f"🚫 Failed to load job search page: {e}")
#                 continue

#             while True:
#                 try:
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
#                     )
#                 except:
#                     print("⚠️ Job container did not load.")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
#                 print(f"📄 Found {len(cards)} job cards.")

#                 for card in cards:
#                     try:
#                         title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text.strip()
#                         if not is_tech_job(title):
#                             continue

#                         company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
#                         location_text = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
#                         job_state = location_text.lower()
#                         href = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href") or ""
#                         job_url = href if href.startswith("http") else f"{base_url}{href}"

#                         driver.execute_script("window.open(arguments[0]);", job_url)
#                         time.sleep(1)

#                         try:
#                             handles = driver.window_handles
#                             driver.switch_to.window(handles[-1])
#                             WebDriverWait(driver, 7).until(
#                                 EC.presence_of_element_located((By.ID, "jobDescriptionText"))
#                             )
#                             description = driver.find_element(By.ID, "jobDescriptionText").text.strip()
#                         except:
#                             description = "N/A"
#                         finally:
#                             try:
#                                 driver.close()
#                                 handles = driver.window_handles
#                                 if handles:
#                                     driver.switch_to.window(handles[0])
#                                 else:
#                                     raise Exception("💀 No remaining tabs. Session likely dead.")
#                             except Exception as e:
#                                 print(f"⚠️ Could not return to main window: {e}. Restarting driver.")
#                                 try: driver.quit()
#                                 except: pass
#                                 driver = configure_webdriver()
#                                 break  # Exit inner loop and retry keyword cleanly



#                         matched_skills = extract_skills(description, skill_matrix)

#                         job = {
#                             "title": title,
#                             "company": company,
#                             "job_location": location_text,
#                             "job_state": job_state,
#                             "date": datetime.today().date(),
#                             "site": "Indeed",
#                             "job_description": description,
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword,
#                             "skills": matched_skills,
#                         }

#                         insert_job_to_db(job)
#                         jobs_scraped.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing job: {e}")
#                         traceback.print_exc()
#                         continue

#                 try:
#                     next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
#                     if next_btn.is_enabled():
#                         driver.execute_script("arguments[0].click();", next_btn)
#                         time.sleep(2)
#                     else:
#                         break
#                 except:
#                     break

#     finally:
#         try: driver.quit()
#         except: pass

#     if jobs_scraped:
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         with open(f"crawl4ai_indeed_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=list(jobs_scraped[0].keys()))
#             writer.writeheader()
#             writer.writerows(jobs_scraped)
#         print(f"📁 Saved to crawl4ai_indeed_jobs_{ts}.csv")

#     cleanup(days)
#     print(f"\n✅ Crawl4AI (Indeed) collected {len(jobs_scraped)} jobs.")
#     return jobs_scraped


if __name__ == "__main__":
    jobs = get_jobs_from_crawl4ai()
    print(f"🎯 Finished scraping. {len(jobs)} jobs returned.")

# import sys
# import time
# import random
# import csv
# import traceback
# from datetime import datetime, timedelta

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from app.services.skills import extract_skills
# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.scraper.indeed_scraper import TECH_KEYWORDS 

# LOCATION = "remote"
# MAX_DAYS = 5


# def configure_webdriver():
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
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO jobs (
#                 id, title, company, job_location, job_state, date, site,
#                 job_description, salary, url, applied, search_term, inserted_at
#             ) VALUES (
#                 gen_random_uuid(), %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, NOW()
#             )
#             ON CONFLICT (url) DO NOTHING;
#         """, (
#             job["title"], job["company"], job["job_location"], job["job_state"],
#             job["date"], job["site"], job["job_description"], job["salary"],
#             job["url"], job["applied"], job["search_term"]
#         ))
#         conn.commit()
#     except Exception as e:
#         print(f"❌ DB insert error: {e}")
#         traceback.print_exc()
#     finally:
#         cur.close()
#         conn.close()


# def get_jobs_from_crawl4ai(location=LOCATION, days=MAX_DAYS):
#     print(f"🌐 Crawl4AI (Indeed) → {location} (last {days} days)")
#     base_url = "https://www.indeed.com"
#     driver = configure_webdriver()
#     jobs_scraped = []

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 '{keyword}'")
#             url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"

#             try:
#                 if not driver.session_id:
#                     raise Exception("WebDriver session invalid")

#                 driver.get(url)
#                 with open(f"debug_{keyword.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
#                     f.write(driver.page_source)
#                     print(f"📝 Saved HTML snapshot for '{keyword}'")
#                 time.sleep(2)

#             except Exception as e:
#                 print(f"🚫 Failed to load job search page: {e}")
#                 break

#             while True:
#                 try:
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
#                     )
#                 except:
#                     print("⚠️ Job container did not load.")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
#                 print(f"📄 Found {len(cards)} job cards.")

#                 for card in cards:
#                     try:
#                         title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text.strip()
#                         if not is_tech_job(title):
#                             continue

#                         company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
#                         location_text = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
#                         job_state = location_text.lower()

#                         href = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href") or ""
#                         job_url = href if href.startswith("http") else f"{base_url}{href}"

#                         # Open in new tab
#                         driver.execute_script("window.open(arguments[0]);", job_url)
#                         time.sleep(1)

#                         try:
#                             handles = driver.window_handles
#                             driver.switch_to.window(handles[-1])
#                             WebDriverWait(driver, 7).until(
#                                 EC.presence_of_element_located((By.ID, "jobDescriptionText"))
#                             )
#                             description = driver.find_element(By.ID, "jobDescriptionText").text.strip()
#                         except:
#                             description = "N/A"
#                         finally:
#                             try:
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
#                             except:
#                                 print("⚠️ Could not switch back to main window. Ending loop.")
#                                 break

#                         job = {
#                             "title": title,
#                             "company": company,
#                             "job_location": location_text,
#                             "job_state": job_state,
#                             "date": datetime.today().date(),
#                             "site": "Indeed",
#                             "job_description": description,
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword
#                         }

#                         insert_job_to_db(job)
#                         jobs_scraped.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing job: {e}")
#                         traceback.print_exc()
#                         continue

#                 try:
#                     next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
#                     if next_btn.is_enabled():
#                         driver.execute_script("arguments[0].click();", next_btn)
#                         time.sleep(2)
#                     else:
#                         break
#                 except:
#                     break

#     finally:
#         try:
#             driver.quit()
#         except:
#             pass

#     if jobs_scraped:
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         with open(f"crawl4ai_indeed_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=list(jobs_scraped[0].keys()))
#             writer.writeheader()
#             writer.writerows(jobs_scraped)
#         print(f"📁 Saved to crawl4ai_indeed_jobs_{ts}.csv")

#     cleanup(days)
#     print(f"\n✅ Crawl4AI (Indeed) collected {len(jobs_scraped)} jobs.")
#     return jobs_scraped

# if __name__ == "__main__":
#     jobs = get_jobs_from_crawl4ai()
#     print(f"🎯 Finished scraping. {len(jobs)} jobs returned.")








# import sys
# import time
# import random
# import csv
# import traceback
# from datetime import datetime, timedelta

# from ..utils.write_jobs import write_jobs_csv
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.db.cleanup import cleanup
# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.utils.skill_utils import load_flat_skills, extract_flat_skills

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


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


# def get_jobs_from_crawl4ai(location=LOCATION, days=MAX_DAYS):
#     print(f"🌐 Crawl4AI (Indeed) → {location} (last {days} days)")
#     base_url = "https://www.indeed.com"
#     driver = configure_driver()
#     jobs_scraped = []

#     # ✅ Load skills once
#     skill_list = load_flat_skills("app/resources/skills.txt")

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 '{keyword}'")
#             url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"
#             driver.get(url)

#             with open(f"debug_{keyword.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
#                 f.write(driver.page_source)
#                 print(f"📝 Saved HTML snapshot for '{keyword}'")

#             time.sleep(3)

#             while True:
#                 try:
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'mainContentTable')]"))
#                     )
#                 except:
#                     print("⚠️ Container did not load.")
#                     break

#                 cards = driver.find_elements(By.XPATH, "//table[contains(@class,'mainContentTable')]")

#                 for table in cards:
#                     try:
#                         title = table.find_element(By.XPATH, ".//h2[contains(@class, 'jobTitle')]/a/span").text.strip()
#                         if not is_tech_job(title):
#                             continue

#                         company = table.find_element(By.XPATH, ".//span[@data-testid='company-name']").text.strip()
#                         job_location = table.find_element(By.XPATH, ".//div[@data-testid='text-location']").text.strip()
#                         job_state = job_location.split(",")[-1].strip() if "," in job_location else job_location

#                         try:
#                             date_posted = parse_date(
#                                 table.find_element(By.XPATH, ".//span[contains(text(), 'Posted') or contains(text(), 'Just posted')]").text.strip()
#                             )
#                         except:
#                             date_posted = datetime.today().date()

#                         job_url = f"{base_url}/viewjob?jk={table.find_element(By.XPATH, './/a[@data-jk]').get_attribute('data-jk') or ''}"

#                         driver.execute_script("arguments[0].scrollIntoView(true);", table)
#                         table.find_element(By.XPATH, ".//a[@data-jk]").click()
#                         time.sleep(2)

#                         try:
#                             full_desc = WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.ID, "jobDescriptionText"))
#                             ).text.strip()
#                         except:
#                             full_desc = "N/A"

#                         skills = extract_flat_skills(full_desc, skill_list)

#                         job = {
#                             "title": title,
#                             "company": company,
#                             "job_location": job_location,
#                             "job_state": job_state,
#                             "date": date_posted,
#                             "site": "Indeed",
#                             "job_description": full_desc,
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "saved": False,
#                             "search_term": keyword,
#                             "skills": skills,
#                             "priority": 0,
#                             "status": "new",
#                             "category": None,
#                             "inserted_at": datetime.utcnow(),
#                             "last_verified": None,
#                             "user_id": None
#                         }
#                         job["date"] = datetime.today().date()
#                         insert_job_to_db(job)
#                         jobs_scraped.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing job: {e}")
#                         traceback.print_exc()
#                         continue

#                 try:
#                     next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
#                     if next_btn.is_enabled():
#                         driver.execute_script("arguments[0].click();", next_btn)
#                         time.sleep(2)
#                     else:
#                         break
#                 except:
#                     break

#     finally:
#         driver.quit()

#     if jobs_scraped:
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         with open(f"crawl4ai_indeed_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=list(jobs_scraped[0].keys()))
#             writer.writeheader()
#             writer.writerows(jobs_scraped)
#         print(f"📁 Saved to crawl4ai_indeed_jobs_{ts}.csv")

#     cleanup(days)
#     print(f"\n✅ Crawl4AI (Indeed) collected {len(jobs_scraped)} jobs.")
#     return jobs_scraped


# def main():
#     print("📡 Indeed Crawler Starting…")
#     jobs = get_jobs_from_crawl4ai()
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")

#     write_jobs_csv(jobs, folder_name="debugged", label="indeed_crawl")
#     print("🔁 Ensuring database is synced with CSV...")
#     sync_job_data_folder_to_supabase(folder="server/job_data")

#     cleanup(MAX_DAYS)


# if __name__ == "__main__":
#     main()












# import sys
# import time
# import random
# import csv
# import traceback
# from datetime import datetime, timedelta
# from app.utils.write_jobs import write_jobs_csv
# from app.db.sync_jobs import insert_job_to_db
# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from app.db.cleanup import cleanup
# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.db.sync_jobs import sync_job_data_folder_to_supabase
# from app.utils.skill_utils import load_flat_skills, extract_flat_skills

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

# def get_jobs_from_crawl4ai(location=LOCATION, days=MAX_DAYS):
#     print(f"🌐 Crawl4AI (Indeed) → {location} (last {days} days)")
#     base_url = "https://www.indeed.com"
#     driver = configure_driver()
#     jobs_scraped = []

#     skill_list = load_flat_skills("app/resources/skills.txt")

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 '{keyword}'")
#             url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"
#             driver.get(url)

#             with open(f"debug_{keyword.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
#                 f.write(driver.page_source)
#                 print(f"📝 Saved HTML snapshot for '{keyword}'")

#             time.sleep(3)

#             while True:
#                 try:
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'mainContentTable')]"))
#                     )
#                 except:
#                     print("⚠️ Container did not load.")
#                     break

#                 cards = driver.find_elements(By.XPATH, "//table[contains(@class,'mainContentTable')]")

#                 for table in cards:
#                     try:
#                         title_el = table.find_element(By.XPATH, ".//h2[contains(@class, 'jobTitle')]/a/span")
#                         title = title_el.text.strip()
#                         if not is_tech_job(title):
#                             continue

#                         company_el = table.find_element(By.XPATH, ".//span[@data-testid='company-name']")
#                         company = company_el.text.strip()

#                         location_el = table.find_element(By.XPATH, ".//div[@data-testid='text-location']")
#                         job_location = location_el.text.strip()
#                         job_state = job_location.split(",")[-1].strip() if "," in job_location else job_location

#                         try:
#                             date_el = table.find_element(By.XPATH, ".//span[contains(text(), 'Posted') or contains(text(), 'Just posted')]")
#                             date_posted = parse_date(date_el.text.strip())
#                         except:
#                             date_posted = datetime.today().date()

#                         link_el = table.find_element(By.XPATH, ".//a[@data-jk]")
#                         job_url = f"{base_url}/viewjob?jk={link_el.get_attribute('data-jk') or ''}"

#                         driver.execute_script("arguments[0].scrollIntoView(true);", link_el)
#                         driver.execute_script("arguments[0].click();", link_el)
#                         time.sleep(2)

#                         try:
#                             desc_el = WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.ID, "jobDescriptionText"))
#                             )
#                             full_desc = desc_el.text.strip()
#                         except:
#                             full_desc = "N/A"

#                         skills = extract_flat_skills(full_desc, skill_list)

#                         job = {
#                             "title": title,
#                             "company": company,
#                             "job_location": job_location,
#                             "job_state": job_state,
#                             "date": date_posted,
#                             "site": "Indeed",
#                             "job_description": full_desc,
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "saved": False,
#                             "search_term": keyword,
#                             "skills": skills,
#                             "priority": 0,
#                             "status": "new",
#                             "category": None,
#                             "inserted_at": datetime.utcnow(),
#                             "last_verified": None,
#                             "user_id": None
#                         }

#                         insert_job_to_db(job)
#                         jobs_scraped.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing job: {e}")
#                         traceback.print_exc()
#                         continue

#                 try:
#                     next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
#                     if next_btn.is_enabled():
#                         driver.execute_script("arguments[0].click();", next_btn)
#                         time.sleep(2)
#                     else:
#                         break
#                 except:
#                     break

#     finally:
#         driver.quit()

#     if jobs_scraped:
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         with open(f"crawl4ai_indeed_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=list(jobs_scraped[0].keys()))
#             writer.writeheader()
#             writer.writerows(jobs_scraped)
#         print(f"📁 Saved to crawl4ai_indeed_jobs_{ts}.csv")

#     cleanup(days)
#     print(f"\n✅ Crawl4AI (Indeed) collected {len(jobs_scraped)} jobs.")
#     return jobs_scraped

# def main():
#     print("📡 Indeed Crawler Starting…")
#     jobs = get_jobs_from_crawl4ai()
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")
    
#     write_jobs_csv(jobs, folder_name="debugged", label="indeed_crawl")
#     print("🔁 Ensuring database is synced with CSV...")
#     sync_job_data_folder_to_supabase(folder="server/job_data")
    
#     cleanup(MAX_DAYS)

# if __name__ == "__main__":
#     main()

