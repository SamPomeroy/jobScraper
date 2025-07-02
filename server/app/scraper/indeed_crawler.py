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
