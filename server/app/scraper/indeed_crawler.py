import sys
import time
import random
import csv
import traceback
from datetime import datetime, timedelta

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.db.connect_database import get_db_connection
from app.db.cleanup import cleanup
from app.scraper.indeed_scraper import TECH_KEYWORDS 

LOCATION = "remote"
MAX_DAYS = 5


def configure_webdriver():
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


def parse_date(raw: str):
    raw = raw.lower()
    if "today" in raw or "just posted" in raw:
        return datetime.today().date()
    try:
        days_ago = int(raw.strip().split()[0])
        return datetime.today().date() - timedelta(days=days_ago)
    except:
        return datetime.today().date()


def is_tech_job(title: str) -> bool:
    return any(keyword.lower() in title.lower() for keyword in TECH_KEYWORDS)


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
            ON CONFLICT (url) DO NOTHING;
        """, (
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


def get_jobs_from_crawl4ai(location=LOCATION, days=MAX_DAYS):
    print(f"🌐 Crawl4AI (Indeed) → {location} (last {days} days)")
    base_url = "https://www.indeed.com"
    driver = configure_webdriver()
    jobs_scraped = []

    try:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 '{keyword}'")
            url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"
            driver.get(url)

            # Save snapshot for debugging
            with open(f"debug_{keyword.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
                print(f"📝 Saved HTML snapshot for '{keyword}'")

            time.sleep(3)

            while True:
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'mainContentTable')]"))
                    )
                except:
                    print("⚠️ Container did not load.")
                    break

                cards = driver.find_elements(
                    By.XPATH, "//table[contains(@class,'mainContentTable')]"
                )

                for table in cards:
                    try:
                        title_el = table.find_element(By.XPATH, ".//h2[contains(@class, 'jobTitle')]/a/span")
                        title = title_el.text.strip()
                        if not is_tech_job(title):
                            continue

                        company_el = table.find_element(By.XPATH, ".//span[@data-testid='company-name']")
                        location_el = table.find_element(By.XPATH, ".//div[@data-testid='text-location']")
                        try:
                            # Try any known or new selector for posted date
                            date_el = table.find_element(By.XPATH, ".//span[contains(text(), 'Posted') or contains(text(), 'Just posted')]")
                            date_posted = parse_date(date_el.text.strip())
                        except:
                                date_posted = datetime.today().date()
                        link_el = table.find_element(By.XPATH, ".//a[@data-jk]")

                        job_url = f"{base_url}/viewjob?jk={link_el.get_attribute('data-jk') or ''}"
                        # date_posted = parse_date(date_el.text.strip())

                        driver.execute_script("arguments[0].scrollIntoView(true);", link_el)
                        driver.execute_script("arguments[0].click();", link_el)
                        time.sleep(2)

                        try:
                            desc_el = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
                            )
                            description = desc_el.text.strip()
                        except:
                            description = "N/A"

                        job = {
                            "title": title,
                            "company": company_el.text.strip() or "N/A",
                            "job_location": location_el.text.strip() or location,
                            "job_state": location.lower(),
                            "date": date_posted,
                            "site": "Indeed",
                            "job_description": description,
                            "salary": "N/A",
                            "url": job_url,
                            "applied": False,
                            "search_term": keyword
                        }

                        insert_job_to_db(job)
                        jobs_scraped.append(job)

                    except Exception as e:
                        print(f"❌ Error parsing job: {e}")
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
        driver.quit()

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



# import sys
# import time
# import random
# import csv
# import traceback
# from datetime import datetime, timedelta
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver as uc
# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.scraper.indeed_scraper import TECH_KEYWORDS  # reuse shared keywords

# LOCATION = "remote"
# PAGES_PER_KEYWORD = 2
# MAX_DAYS = 15

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
#             driver.get(url)
#             with open(f"debug_{keyword.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
#                 f.write(driver.page_source)
#                 print(f"📝 Saved HTML snapshot for '{keyword}'")

#             time.sleep(2)

#             while True:
#                 try:
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'mainContentTable')]"))
#                     )
#                 except:
#                     print("⚠️ Container did not load.")
#                     break

#                 cards = driver.find_elements(
#                     By.XPATH, "//ul[contains(@class,'jobsearch-ResultsList')]/li//table[contains(@class,'mainContentTable')]"
#                 )

#                 for table in cards:
#                     try:
#                         title_el = table.find_element(By.XPATH, ".//h2[contains(@class, 'jobTitle')]/a/span")
#                         title = title_el.text.strip()
#                         if not is_tech_job(title):
#                             continue

#                         company_el = table.find_element(By.XPATH, ".//span[@data-testid='company-name']")
#                         location_el = table.find_element(By.XPATH, ".//div[@data-testid='text-location']")
#                         date_el = table.find_element(By.XPATH, ".//span[contains(@class, 'date')]")
#                         link_el = table.find_element(By.XPATH, ".//a[@data-jk]")

#                         job_url = f"{base_url}/viewjob?jk={link_el.get_attribute('data-jk') or ''}"
#                         date_posted = parse_date(date_el.text.strip())

#                         driver.execute_script("arguments[0].scrollIntoView(true);", table)
#                         link_el.click()
#                         time.sleep(2)

#                         try:
#                             desc_el = WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.ID, "jobDescriptionText"))
#                             )
#                             description = desc_el.text.strip()
#                         except:
#                             description = "N/A"

#                         job = {
#                             "title": title,
#                             "company": company_el.text.strip() or "N/A",
#                             "job_location": location_el.text.strip() or location,
#                             "job_state": location.lower(),
#                             "date": date_posted,
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









# import sys
# import time
# import uuid
# import random
# import traceback
# import pandas as pd
# import csv
# from datetime import datetime, timedelta

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver as uc

# from db.connect_database import get_db_connection
# from db.cleanup import cleanup

# # ✅ Dynamic keyword input
# TECH_KEYWORDS = sys.argv[1].split(",") if len(sys.argv) > 1 else [
#     "software engineer", "front-end developer", "back-end developer",
#     # ... add the rest of your keywords ...
#     "web content manager"
# ]

# LOCATION = "remote"
# PAGES_PER_KEYWORD = 2
# MAX_DAYS = 15

# def configure_webdriver():
#     options = uc.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     return uc.Chrome(options=options)

# def is_tech_job(title: str) -> bool:
#     return any(keyword.lower() in title.lower() for keyword in TECH_KEYWORDS)

# def parse_date(raw: str):
#     if "today" in raw.lower() or "just posted" in raw.lower():
#         return datetime.today().date()
#     try:
#         days_ago = int(raw.strip().split()[0])
#         return datetime.today().date() - timedelta(days=days_ago)
#     except:
#         return datetime.today().date()

# def insert_job_to_db(job: dict):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO jobs (
#                 id, title, company, job_location, job_state, date, site,
#                 job_description, salary, url, applied, search_term, inserted_at
#             )
#             VALUES (
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

# def scrape_jobs(location, days=MAX_DAYS):
#     base_url = "https://www.indeed.com"
#     driver = configure_webdriver()
#     jobs_scraped = []

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'...")
#             url = f"{base_url}/jobs?q={'+'.join(keyword.split())}&l={location}&fromage={days}&forceLocation=0"
#             driver.get(url)
#             time.sleep(2)

#             while True:
#                 try:
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'mainContentTable')]"))
#                     )
#                 except:
#                     print("⚠️ Job container did not load.")
#                     break

#                 job_cards = driver.find_elements(
#                     By.XPATH, "//ul[contains(@class,'jobsearch-ResultsList')]/li//table[contains(@class,'mainContentTable')]"
#                 )

#                 for table in job_cards:
#                     try:
#                         title_el = table.find_element(By.XPATH, ".//h2[contains(@class, 'jobTitle')]/a/span")
#                         title = title_el.text.strip()
#                         if not is_tech_job(title):
#                             continue

#                         company_el = table.find_element(By.XPATH, ".//span[@data-testid='company-name']")
#                         location_el = table.find_element(By.XPATH, ".//div[@data-testid='text-location']")
#                         date_el = table.find_element(By.XPATH, ".//span[contains(@class, 'date')]")
#                         link_el = table.find_element(By.XPATH, ".//a[@data-jk]")

#                         job_url = f"{base_url}/viewjob?jk={link_el.get_attribute('data-jk') or ''}"
#                         date_posted = parse_date(date_el.text.strip())

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
#                         driver.execute_script("arguments[0].click();", next_btn)
#                         time.sleep(2)
#                     else:
#                         break
#                 except:
#                     break

#     finally:
#         if driver:
#             driver.quit()

    
#     if jobs_scraped:
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         with open(f"crawl4ai_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=list(jobs_scraped[0].keys()))
#             writer.writeheader()
#             writer.writerows(jobs_scraped)
#         print(f"📁 CSV saved to crawl4ai_jobs_{ts}.csv")

#     cleanup(days)
#     print(f"\n✅ Crawl4AI finished. Total jobs collected: {len(jobs_scraped)}")
#     return jobs_scraped


# # import time
# import random
# from datetime import datetime
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver

# from db.connect_database import get_db_connection
# from scraper.indeed_scraper import TECH_KEYWORDS, is_tech_job, parse_date

# def configure_webdriver():
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     driver = webdriver.Chrome(options=options)
#     return driver

# def insert_job_to_db(job):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO jobs (
#                 id, title, company, job_location, job_state, date, site,
#                 job_description, salary, url, applied, search_term
#             ) VALUES (
#                 gen_random_uuid(), %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s
#             ) ON CONFLICT (url) DO NOTHING
#         """, (
#             job["title"], job["company"], job["job_location"], job["job_state"],
#             job["date"], job["site"], job["job_description"], job["salary"],
#             job["url"], job["applied"], job["search_term"]
#         ))
#         conn.commit()
#     except Exception as e:
#         print(f"❌ DB insert error: {e}")
#     finally:
#         cur.close()
#         conn.close()

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

#                         jk_value = link_el.get_attribute("data-jk")
#                         if jk_value:
#                             job_url = base_url + "/viewjob?jk=" + jk_value
#                         else:
#                             job_url = ""
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
#                 pass

#     print(f"\n✅ Crawl4AI finished. Total jobs collected: {len(jobs_scraped)}")
#     return jobs_scraped
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
