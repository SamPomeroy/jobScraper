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