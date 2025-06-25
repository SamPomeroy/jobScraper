# import time
# import uuid
# import csv
# import random
# import traceback
# import pandas as pd
# from datetime import datetime
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from IndeedJobScraper.app.db.db_connect import get_db_connection  # your existing DB helper

# BASE_URL = "https://www.careerbuilder.com"
# HEADERS = {"User-Agent": "Mozilla/5.0"}
# SEARCH_TERM = "frontend developer"
# LOCATION = "remote"

# def insert_job_to_db(job):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO jobs (
#                 id, title, company, job_location, job_state, date, site,
#                 job_description, salary, url, applied, search_term
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             ON CONFLICT (url) DO NOTHING
#         """, (
#             str(uuid.uuid4()), job["title"], job["company"], job["job_location"],
#             job["job_state"], job["date"], job["site"], job["job_description"],
#             job["salary"], job["url"], job["applied"], job["search_term"]
#         ))
#         conn.commit()
#     except Exception as e:
#         print(f"❌ DB insert error: {e}")
#     finally:
#         cur.close()
#         conn.close()

# def scrape_careerbuilder_jobs(search_term, location="remote", pages=1):
#     options = Options()
#     options.add_argument("--headless")
#     driver = webdriver.Chrome(options=options)
#     jobs = []

#     try:
#         for page in range(1, pages + 1):
#             url = f"{BASE_URL}/jobs?keywords={'+'.join(search_term.split())}&location={location}&page_number={page}"
#             driver.get(url)
#             time.sleep(random.uniform(2, 3))

#             soup = BeautifulSoup(driver.page_source, "html.parser")
#             listings = soup.select("li.data-results-content-parent")

#             for li in listings:
#                 try:
#                     title = li.select_one(".data-results-title").text.strip()
#                     company = li.select_one(".data-details span").text.strip()
#                     location_text = li.select(".data-details span")[1].text.strip()
#                     job_url = BASE_URL + li.select_one("a[data-job-did]")["href"]
#                     description = li.select_one(".data-snapshot .block").text.strip()

#                     job = {
#                         "title": title.lower(),
#                         "company": company.lower(),
#                         "job_location": location_text.lower(),
#                         "job_state": location_text.split(",")[-1].strip().lower() if "," in location_text else location.lower(),
#                         "date": datetime.today().date(),
#                         "site": "careerbuilder",
#                         "job_description": description,
#                         "salary": "N/A",
#                         "url": job_url,
#                         "applied": False,
#                         "search_term": search_term
#                     }

#                     insert_job_to_db(job)
#                     jobs.append(job)

#                 except Exception as e:
#                     print(f"⚠️ Error parsing job: {e}")
#                     continue

#     finally:
#         if driver:
#             try:
#                 driver.quit()
#             except Exception:
#                 pass  # Silences WinError 6


#     return jobs

# import time
# import random
# from datetime import datetime
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
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
#         driver.quit()

#     print(f"\n✅ Crawl4AI finished. Total jobs collected: {len(jobs_scraped)}")
#     return jobs_scraped
# import sys
# import time
# import uuid
# import random
# import traceback
# import csv

# from datetime import datetime
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver as uc

# from career_crawler import 
# from db.connect_database import get_db_connection

# # ✅ Keywords come from CLI or default list
# TECH_KEYWORDS = (
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
# )
# LOCATION = "remote"
# PAGES_PER_KEYWORD = 2   # pages to crawl per keyword

# def configure_webdriver():
#     opts = uc.ChromeOptions()
#     opts.add_argument("--start-maximized")
#     opts.add_argument("--disable-blink-features=AutomationControlled")
#     opts.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36"
#     )
#     for i in range(3):
#         try:
#             return uc.Chrome(options=opts, headless=False)
#         except Exception as e:
#             print(f"🚧 Driver init failed (attempt {i+1}): {e}")
#             time.sleep(2)
#     raise RuntimeError("Chrome driver failed to start after 3 attempts")

# def insert_job_to_db(job: dict):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO jobs
#               (id, title, company, job_location, job_state, date, site,
#                job_description, salary, url, applied, search_term)
#             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#             ON CONFLICT (url) DO NOTHING
#         """, (
#             str(uuid.uuid4()),
#             job["title"], job["company"],
#             job["job_location"], job["job_state"],
#             job["date"], job["site"],
#             job["job_description"], job["salary"],
#             job["url"], job["applied"],
#             job["search_term"]
#         ))
#         conn.commit()
#     except Exception as e:
#         print("❌ DB insert error:", e)
#         traceback.print_exc()
#     finally:
#         cur.close()
#         conn.close()

# def scrape_careerbuilder(location: str, pages: int = PAGES_PER_KEYWORD):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_webdriver()
#     all_jobs = []

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 search_url = (
#                     f"{base_url}/jobs?"
#                     f"keywords={'+'.join(keyword.split())}&"
#                     f"location={location}&"
#                     f"page_number={page}"
#                 )
#                 driver.get(search_url)

#                 # wait for cards to appear
#                 try:
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located(
#                             (By.CSS_SELECTOR, "li.data-results-content-parent")
#                         )
#                     )
#                 except:
#                     print("⚠️ No job cards found, skipping to next keyword/page")
#                     break

#                 time.sleep(random.uniform(1.0, 2.0))
#                 cards = driver.find_elements(
#                     By.CSS_SELECTOR, "li.data-results-content-parent"
#                 )
#                 print(f"🧾 Found {len(cards)} cards (page {page})")

#                 for card in cards:
#                     try:
#                         # Title
#                         title = card.find_element(
#                             By.CSS_SELECTOR, ".data-results-title"
#                         ).text.strip()

#                         # Company / Location
#                         details = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = details[0].text.strip() if details else "N/A"
#                         job_location = details[1].text.strip() if len(details) > 1 else location
#                         job_state = job_location.lower()

#                         # Open detail page in new tab for full description
#                         link_el = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
#                         href = link_el.get_attribute("href") or ""
#                         if not href:
#                             continue
#                         job_url = href if href.startswith("http") else base_url + href

#                         # new tab
#                         driver.execute_script("window.open(arguments[0])", job_url)
#                         driver.switch_to.window(driver.window_handles[-1])
#                         time.sleep(1)
#                         try:
#                             WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                             )
#                             full_desc = driver.find_element(
#                                 By.CSS_SELECTOR, "#jdp_description"
#                             ).text.strip()
#                         except:
#                             full_desc = ""
#                         # close detail tab
#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])

#                         job = {
#                             "title":           title,
#                             "company":         company,
#                             "job_location":    job_location,
#                             "job_state":       job_state,
#                             "date":            datetime.today().date(),
#                             "site":            "CareerBuilder",
#                             "job_description": full_desc or "",
#                             "salary":          "N/A",
#                             "url":             job_url,
#                             "applied":         False,
#                             "search_term":     keyword
#                         }

#                         insert_job_to_db(job)
#                         all_jobs.append(job)

#                     except Exception as e:
#                         print("❌ Error parsing card:", e)
#                         continue

#     finally:
#         driver.quit()

#     return all_jobs

# def main():
#     print("📡 CareerBuilder Scraper Starting…")
#     jobs = scrape_careerbuilder(LOCATION)
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")

#     if jobs:
#         ts = datetime.now




import sys
import time
import uuid
import random
import traceback
import csv
from app.utils.file_helpers import write_jobs_to_csv
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# <-- import your database helper
from app.db.connect_database import get_db_connection

# ✅ Keywords come from CLI or default list
TECH_KEYWORDS = (
    sys.argv[1].split(",") if len(sys.argv) > 1 else [
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
)
LOCATION = "remote"
PAGES_PER_KEYWORD = 2   # pages to crawl per keyword

def configure_webdriver():
    opts = uc.ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36"
    )
    for i in range(3):
        try:
            return uc.Chrome(options=opts, headless=False)
        except Exception as e:
            print(f"🚧 Driver init failed (attempt {i+1}): {e}")
            time.sleep(2)
    raise RuntimeError("Chrome driver failed to start after 3 attempts")

def insert_job_to_db(job: dict):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO jobs
              (id, title, company, job_location, job_state, date, site,
               job_description, salary, url, applied, search_term)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (url) DO NOTHING
        """, (
            str(uuid.uuid4()),
            job["title"], job["company"],
            job["job_location"], job["job_state"],
            job["date"], job["site"],
            job["job_description"], job["salary"],
            job["url"], job["applied"],
            job["search_term"]
        ))
        conn.commit()
    except Exception as e:
        print("❌ DB insert error:", e)
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()

def scrape_careerbuilder(location: str, pages: int = PAGES_PER_KEYWORD):
    base_url = "https://www.careerbuilder.com"
    driver = configure_webdriver()
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
                driver.get(search_url)

                # wait for cards to appear
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "li.data-results-content-parent")
                        )
                    )
                except:
                    print("⚠️ No job cards found, skipping to next keyword/page")
                    break

                time.sleep(random.uniform(1.0, 2.0))
                cards = driver.find_elements(
                    By.CSS_SELECTOR, "li.data-results-content-parent"
                )
                print(f"🧾 Found {len(cards)} cards (page {page})")

                for card in cards:
                    try:
                        # Title
                        title = card.find_element(
                            By.CSS_SELECTOR, ".data-results-title"
                        ).text.strip()

                        # Company / Location
                        details = card.find_elements(By.CSS_SELECTOR, ".data-details span")
                        company = details[0].text.strip() if details else "N/A"
                        job_location = details[1].text.strip() if len(details) > 1 else location
                        job_state = job_location.lower()

                        # Open detail page in new tab for full description
                        link_el = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
                        href = link_el.get_attribute("href") or ""
                        if not href:
                            continue
                        job_url = href if href.startswith("http") else base_url + href

                        # new tab
                        driver.execute_script("window.open(arguments[0])", job_url)
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(1)
                        try:
                            WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
                            )
                            full_desc = driver.find_element(
                                By.CSS_SELECTOR, "#jdp_description"
                            ).text.strip()
                        except:
                            full_desc = ""
                        # close detail tab
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                        job = {
                            "title":           title,
                            "company":         company,
                            "job_location":    job_location,
                            "job_state":       job_state,
                            "date":            datetime.today().date(),
                            "site":            "CareerBuilder",
                            "job_description": full_desc or "",
                            "salary":          "N/A",
                            "url":             job_url,
                            "applied":         False,
                            "search_term":     keyword
                        }

                        insert_job_to_db(job)
                        career_jobs_scraped.append(job)
                        write_jobs_to_csv(career_jobs_scraped, prefix="careerbuilder_jobs")

                    except Exception as e:
                        print("❌ Error parsing card:", e)
                        continue

    finally:
        driver.quit()

    return career_jobs_scraped
# def main():
#     print("📡 CareerBuilder Scraper Starting…")
#     jobs = scrape_careerbuilder(LOCATION)
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")

#     if jobs:
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         with open(f"careerbuilder_jobs_{ts}.csv", "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
#             writer.writeheader()
#             writer.writerows(jobs)
#         print(f"📁 Jobs saved to careerbuilder_jobs_{ts}.csv")

# if __name__ == "__main__":
#     main()

