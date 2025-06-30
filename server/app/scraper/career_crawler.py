# career_crawler.py




import time
import uuid
import traceback
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException

from app.utils.common import TECH_KEYWORDS, LOCATION, PAGES_PER_KEYWORD, MAX_DAYS, configure_driver
from app.db.sync_jobs import insert_job_to_db
from app.db.cleanup import cleanup
from app.utils.write_jobs import write_jobs_csv

def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
    base_url = "https://www.careerbuilder.com"
    driver = configure_driver()
    jobs = []
    seen_urls = set()

    try:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 Crawling '{keyword}' in '{location}'")
            for page in range(1, pages + 1):
                url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

                if not driver or not driver.session_id:
                    print("💥 Restarting WebDriver session...")
                    try: driver.quit()
                    except: pass
                    driver = configure_driver()

                try:
                    driver.get(url)
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
                    )
                except Exception as e:
                    print(f"⚠️ Error loading search page {page} for '{keyword}': {e}")
                    continue

                cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
                print(f"📄 Found {len(cards)} job cards on page {page}")

                for card in cards:
                    try:
                        if not driver or not driver.session_id:
                            raise InvalidSessionIdException("Dead session during card loop")

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

                        job = {
                            "id": str(uuid.uuid4()),
                            "title": title,
                            "company": company,
                            "job_location": job_location,
                            "job_state": job_state,
                            "date": datetime.today().date(),
                            "site": "CareerBuilder",
                            "job_description": "",
                            "salary": "N/A",
                            "url": job_url,
                            "applied": False,
                            "search_term": keyword,
                            "skills": [],  # to be enriched later
                            "skills_by_category": {},  # to be enriched later
                            "priority": 0,
                            "status": "new",
                            "category": None,
                            "inserted_at": datetime.utcnow(),
                            "last_verified": None,
                            "user_id": None
                        }

                        insert_job_to_db(job)
                        jobs.append(job)

                    except InvalidSessionIdException:
                        print("💥 Rebuilding driver mid-loop...")
                        try: driver.quit()
                        except: pass
                        driver = configure_driver()
                        break
                    except Exception as e:
                        print(f"❌ Error parsing job: {e}")
                        traceback.print_exc()
                        continue

    finally:
        try: driver.quit()
        except: pass

        if jobs:
            write_jobs_csv(jobs, folder_name="job_data", label="careerbuilder")
        cleanup(days)
        print(f"\n✅ CareerBuilder crawler collected {len(jobs)} jobs.")

    return jobs
# import time
# import uuid
# import traceback
# from datetime import datetime

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import InvalidSessionIdException

# from app.utils.common import TECH_KEYWORDS, LOCATION, PAGES_PER_KEYWORD, MAX_DAYS, configure_driver

# from app.services.skills import extract_skills_by_category
# from app.utils.skill_utils import extract_flat_skills

# from app.db.sync_jobs import insert_job_to_db
# from app.db.cleanup import cleanup
# from app.utils.write_jobs import write_jobs_csv



# def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Crawling '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 if not driver or not driver.session_id:
#                     print("💥 Restarting WebDriver session...")
#                     try: driver.quit()
#                     except: pass
#                     driver = configure_driver()

#                 try:
#                     driver.get(url)
#                     time.sleep(2)
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Error loading search page {page} for '{keyword}': {e}")
#                     continue

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                 print(f"📄 Found {len(cards)} job cards on page {page}")

#                 for card in cards:
#                     try:
#                         if not driver or not driver.session_id:
#                             raise InvalidSessionIdException("Dead session during card loop")

#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()
#                         href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                         if not href or href in seen_urls:
#                             continue
#                         seen_urls.add(href)
#                         job_url = href if href.startswith("http") else base_url + href

#                         job_text = title  # You could also append job description here if available

#                         flat_skills = extract_flat_skills(job_text, SKILLS["flat"])
#                         categorized_skills = extract_skills_by_category(job_text, SKILLS["matrix"])

#                         job = {
#                             "id": str(uuid.uuid4()),
#                             "title": title,
#                             "company": company,
#                             "job_location": job_location,
#                             "job_state": job_state,
#                             "date": datetime.today().date(),
#                             "site": "CareerBuilder",
#                             "job_description": "",
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword,
#                             "skills": flat_skills,
#                             "skills_by_category": categorized_skills,  # 🧠 Categorized skills
#                             "priority": 0,
#                             "status": "new",
#                             "category": None,
#                             "inserted_at": datetime.utcnow(),
#                             "last_verified": None,
#                             "user_id": None
#                         }

#                         insert_job_to_db(job)
#                         jobs.append(job)

#                     except InvalidSessionIdException:
#                         print("💥 Rebuilding driver mid-loop...")
#                         try: driver.quit()
#                         except: pass
#                         driver = configure_driver()
#                         break
#                     except Exception as e:
#                         print(f"❌ Error parsing job: {e}")
#                         traceback.print_exc()
#                         continue

#     finally:
#         try: driver.quit()
#         except: pass

#         if jobs:
#             write_jobs_csv(jobs, folder_name="job_data", label="careerbuilder")
#         cleanup(days)
#         print(f"\n✅ CareerBuilder crawler collected {len(jobs)} jobs.")

#     return jobs
# import time
# import uuid
# import traceback
# from datetime import datetime

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import InvalidSessionIdException

# from app.utils.common import TECH_KEYWORDS, LOCATION, PAGES_PER_KEYWORD, MAX_DAYS, configure_driver
# from app.utils.skill_utils import load_flat_skills, extract_flat_skills
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.db.cleanup import cleanup
# from app.utils.write_jobs import write_jobs_csv

# skill_list = load_flat_skills("app/resources/skills.txt")
# def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Crawling '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 if not driver or not driver.session_id:
#                     print("💥 Restarting WebDriver session...")
#                     try: driver.quit()
#                     except: pass
#                     driver = configure_driver()

#                 try:
#                     driver.get(url)
#                     time.sleep(2)
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Error loading search page {page} for '{keyword}': {e}")
#                     continue

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                 print(f"📄 Found {len(cards)} job cards on page {page}")

#                 for card in cards:
#                     try:
#                         if not driver or not driver.session_id:
#                             raise InvalidSessionIdException("Dead session during card loop")

#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()
#                         href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                         if not href or href in seen_urls:
#                             continue
#                         seen_urls.add(href)
#                         job_url = href if href.startswith("http") else base_url + href

#                         job = {
#                             "id": str(uuid.uuid4()),
#                             "title": title,
#                             "company": company,
#                             "job_location": job_location,
#                             "job_state": job_state,
#                             "date": datetime.today().date(),
#                             "site": "CareerBuilder",
#                             "job_description": "",
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword,
#                             "skills": extract_flat_skills(title, skill_list),
#                             "priority": 0,
#                             "status": "new",
#                             "category": None,
#                             "inserted_at": datetime.utcnow(),
#                             "last_verified": None,
#                             "user_id": None
#                         }

#                         insert_job_to_db(job)
#                         jobs.append(job)

#                     except InvalidSessionIdException:
#                         print("💥 Rebuilding driver mid-loop...")
#                         try: driver.quit()
#                         except: pass
#                         driver = configure_driver()
#                         break
#                     except Exception as e:
#                         print(f"❌ Error parsing job: {e}")
#                         traceback.print_exc()
#                         continue

#     finally:
#         try: driver.quit()
#         except: pass

#         if jobs:
#            write_jobs_csv(jobs, folder_name="job_data", label="careerbuilder")
#         cleanup(days)
#         print(f"\n✅ CareerBuilder crawler collected {len(jobs)} jobs.")

#     return jobs
# def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Crawling '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"
#                 try:
#                     if not driver.session_id:
#                         print("⚠️ Driver session lost.")
#                         break

#                     driver.get(url)
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Could not load page {page} for '{keyword}': {e}")
#                     continue

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")

#                 for card in cards:
#                     try:
#                         if not driver.session_id:
#                             print("🔥 WebDriver expired.")
#                             break

#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                         if not href or href in seen_urls:
#                             continue

#                         seen_urls.add(href)
#                         job_url = href if href.startswith("http") else base_url + href

#                         job = {
#                             "id": str(uuid.uuid4()),
#                             "title": title,
#                             "company": company,
#                             "job_location": job_location,
#                             "job_state": job_state,
#                             "date": datetime.today().date(),
#                             "site": "CareerBuilder",
#                             "job_description": "",
#                             "salary": "N/A",
#                             "url": job_url,
#                             "applied": False,
#                             "search_term": keyword,
#                             "skills": extract_flat_skills(title, skill_list),
#                             "priority": 0,
#                             "status": "new",
#                             "category": None,
#                             "inserted_at": datetime.utcnow(),
#                             "last_verified": None,
#                             "user_id": None
#                         }

#                         insert_job_to_db(job)
#                         jobs.append(job)

#                     except InvalidSessionIdException:
#                         print("💥 WebDriver crashed mid-card loop.")
#                         break
#                     except Exception as e:
#                         print(f"❌ Error parsing job: {e}")
#                         traceback.print_exc()
#                         continue

#     finally:
#         try:
#             driver.quit()
#         except:
#             pass
#         return jobs

def main():
    print("🕷️ CareerBuilder Crawler starting...")






# import traceback
# from datetime import datetime

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from app.utils.common import TECH_KEYWORDS, LOCATION, PAGES_PER_KEYWORD, MAX_DAYS, configure_driver
# from app.utils.skill_utils import load_flat_skills, extract_flat_skills
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.db.cleanup import cleanup
# from app.utils.write_jobs import write_jobs_csv

# skill_list = load_flat_skills("app/resources/skills.txt")

# def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"
#                 try:
#                     driver.get(url)
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Skipping page {page} for '{keyword}': {e}")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")

#                 for card in cards:
#                     try:
#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                         if not href or href in seen_urls:
#                             continue

#                         seen_urls.add(href)
#                         job_url = href if href.startswith("http") else base_url + href

#                         driver.execute_script("window.open(arguments[0])", job_url)
#                         time.sleep(2)
#                         driver.switch_to.window(driver.window_handles[-1])
#                         time.sleep(2)

#                         try:
#                             WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                             )
#                             description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                         except:
#                             description = ""

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])

#                         skills = extract_flat_skills(description, skill_list)

#                         job = {
#                             "id": str(uuid.uuid4()),
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
#                         jobs.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing job card: {e}")
#                         traceback.print_exc()
#                         continue

#     finally:
#         driver.quit()
#         return jobs

# def main():
#     print("🕷️ Crawling CareerBuilder...")
#     jobs = get_jobs_from_careerbuilder()
#     print(f"\n✅ Total jobs collected: {len(jobs)}")

#     write_jobs_csv(jobs, folder_name="debugged", label="careerbuilder")
#     print("🗃️ Saved to CSV")

#     sync_job_data_folder_to_supabase(folder="server/job_data")
#     print("🔁 Synced to Supabase")

#     cleanup(MAX_DAYS)
#     print("🧼 Cleanup complete")

# if __name__ == "__main__":
#     main()


# import os
# import time
# import uuid
# import traceback
# import random
# from datetime import datetime

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import InvalidSessionIdException

# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.utils.skill_utils import load_flat_skills, extract_flat_skills
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.db.cleanup import cleanup
# from app.utils.write_jobs import write_jobs_csv

# skill_list = load_flat_skills("app/resources/skills.txt")

# # 🧠 Detect Cloudflare challenge page
# def is_cloudflare_blocked(driver):
#     return "Cloudflare" in driver.page_source or "Just a moment..." in driver.page_source or "Ray ID" in driver.page_source

# def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 try:
#                     driver.get(url)
#                     time.sleep(random.uniform(2.5, 5.5))

#                     if is_cloudflare_blocked(driver):
#                         print("🛑 Cloudflare challenge detected — skipping page.")
#                         break

#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Skipping page {page} for '{keyword}': {e}")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                 print(f"📄 Found {len(cards)} cards")

#                 for card in cards:
#                     try:
#                         if not driver.session_id:
#                             print("🔥 WebDriver session invalid — aborting card parsing.")
#                             break

#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                         if not href or href in seen_urls:
#                             continue

#                         seen_urls.add(href)
#                         job_url = href if href.startswith("http") else base_url + href

#                         # 🚪 Clean up extra tabs
#                         while len(driver.window_handles) > 3:
#                             for h in driver.window_handles[1:]:
#                                 try:
#                                     driver.switch_to.window(h)
#                                     driver.close()
#                                 except:
#                                     pass
#                             driver.switch_to.window(driver.window_handles[0])

#                         driver.execute_script("window.open(arguments[0])", job_url)
#                         time.sleep(random.uniform(2.5, 4.5))
#                         driver.switch_to.window(driver.window_handles[-1])
#                         time.sleep(random.uniform(1.5, 3.5))

#                         if is_cloudflare_blocked(driver):
#                             print(f"⚠️ Blocked on job URL: {job_url}")
#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])
#                             continue

#                         try:
#                             WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                             )
#                             description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                         except:
#                             description = ""

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])

#                         skills = extract_flat_skills(description, skill_list)

#                         job = {
#                             "id": str(uuid.uuid4()),
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
#                         jobs.append(job)

#                     except InvalidSessionIdException:
#                         print("🔥 WebDriver session crashed mid-loop.")
#                         break

#                     except Exception as e:
#                         print(f"❌ Error parsing job card: {e}")
#                         traceback.print_exc()
#                         continue

#     finally:
#         driver.quit()
#         return jobs


# def main():
#     print("📡 CareerBuilder Crawler Starting...")
#     jobs = get_jobs_from_careerbuilder()
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")

#     write_jobs_csv(jobs, folder_name="debugged", label="careerbuilder")
#     print("🔁 Syncing CSVs to Supabase...")
#     sync_job_data_folder_to_supabase(folder="server/job_data")

#     print("🧹 Running cleanup...")
#     cleanup(MAX_DAYS)


# if __name__ == "__main__":
#     main()








# import time
# import uuid
# import traceback
# from datetime import datetime

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import InvalidSessionIdException

# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.utils.skill_utils import load_flat_skills, extract_flat_skills
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.db.cleanup import cleanup
# from app.utils.write_jobs import write_jobs_csv

# skill_list = load_flat_skills("app/resources/skills.txt")


# def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 try:
#                     driver.get(url)
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Skipping page {page} for '{keyword}': {e}")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")

#                 for card in cards:
#                     try:
#                         if not driver.session_id:
#                             print("🔥 WebDriver session invalid — aborting card parsing.")
#                             break

#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                         if not href or href in seen_urls:
#                             continue

#                         seen_urls.add(href)
#                         job_url = href if href.startswith("http") else base_url + href

#                         # Clean up extra tabs
#                         while len(driver.window_handles) > 3:
#                             for h in driver.window_handles[1:]:
#                                 try:
#                                     driver.switch_to.window(h)
#                                     driver.close()
#                                 except:
#                                     pass
#                             driver.switch_to.window(driver.window_handles[0])

#                         driver.execute_script("window.open(arguments[0])", job_url)
#                         time.sleep(1)
#                         driver.switch_to.window(driver.window_handles[-1])
#                         time.sleep(2)

#                         try:
#                             WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                             )
#                             description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                         except:
#                             description = ""

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])

#                         skills = extract_flat_skills(description, skill_list)

#                         job = {
#                             "id": str(uuid.uuid4()),
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
#                         jobs.append(job)

#                     except InvalidSessionIdException:
#                         print("🔥 WebDriver session crashed mid-loop.")
#                         break

#                     except Exception as e:
#                         print(f"❌ Error parsing job card: {e}")
#                         traceback.print_exc()
#                         continue

#     finally:
#         driver.quit()
#         return jobs


# def main():
#     print("📡 CareerBuilder Crawler Starting...")
#     jobs = get_jobs_from_careerbuilder()
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")

#     write_jobs_csv(jobs, folder_name="debugged", label="careerbuilder")
#     print("🔁 Syncing CSVs to Supabase...")
#     sync_job_data_folder_to_supabase(folder="server/job_data")

#     print("🧹 Running cleanup...")
#     cleanup(MAX_DAYS)


# if __name__ == "__main__":
#     main()


# import time
# import uuid
# import traceback
# from datetime import datetime

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.utils.skill_utils import load_flat_skills, extract_flat_skills
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.db.cleanup import cleanup
# from app.utils.write_jobs import write_jobs_csv

# skill_list = load_flat_skills("app/resources/skills.txt")


# def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 try:
#                     driver.get(url)
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Skipping page {page} for '{keyword}': {e}")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")

#                 for card in cards:
#                     try:
#                         # 🔒 Session guard
#                         if not driver.session_id:
#                             raise Exception("Driver session invalid")

#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                         if not href or href in seen_urls:
#                             continue

#                         seen_urls.add(href)
#                         job_url = href if href.startswith("http") else base_url + href

#                         # 🧽 Tab hygiene
#                         while len(driver.window_handles) > 3:
#                             for h in driver.window_handles[1:]:
#                                 try:
#                                     driver.switch_to.window(h)
#                                     driver.close()
#                                 except:
#                                     pass
#                             driver.switch_to.window(driver.window_handles[0])

#                         # 🔗 Open job detail page
#                         driver.execute_script("window.open(arguments[0])", job_url)
#                         time.sleep(1)
#                         driver.switch_to.window(driver.window_handles[-1])
#                         time.sleep(2)

#                         try:
#                             WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                             )
#                             description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                         except:
#                             description = ""

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])

#                         skills = extract_flat_skills(description, skill_list)

#                         job = {
#                             "id": str(uuid.uuid4()),
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
#                         jobs.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing job card: {e}")
#                         traceback.print_exc()
#                         continue

#     finally:
#         driver.quit()
#         return jobs


# def main():
#     print("📡 CareerBuilder Crawler Starting...")
#     jobs = get_jobs_from_careerbuilder()
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")

#     write_jobs_csv(jobs, folder_name="debugged", label="careerbuilder")
#     print("🔁 Syncing CSVs to Supabase...")
#     sync_job_data_folder_to_supabase(folder="server/job_data")

#     print("🧹 Running cleanup...")
#     cleanup(MAX_DAYS)


# if __name__ == "__main__":
#     main()





# import os
# import time
# import uuid
# import random
# import csv
# import traceback
# from datetime import datetime, timedelta

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from app.utils.skill_utils import load_flat_skills
# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.services.skills import extract_skills_by_category, load_skill_matrix


# from app.utils.skill_utils import extract_flat_skills

# from app.utils.write_jobs import write_jobs_csv
# skill_list = load_flat_skills("app/resources/skills.txt")
# def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     skill_matrix = load_skill_matrix()
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 try:
#                     driver.get(url)
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Skipping — no job cards found on page {page} for '{keyword}': {e}")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                 for card in cards:
#                     try:
#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                         if not href or href in seen_urls:
#                             continue

#                         seen_urls.add(href)
#                         job_url = href if href.startswith("http") else base_url + href

#                         # Clean up tab overload
#                         if len(driver.window_handles) > 3:
#                             for handle in driver.window_handles[1:]:
#                                 try:
#                                     driver.switch_to.window(handle)
#                                     driver.close()
#                                 except:
#                                     continue
#                             driver.switch_to.window(driver.window_handles[0])

#                         driver.execute_script("window.open(arguments[0])", job_url)
#                         time.sleep(1)
#                         driver.switch_to.window(driver.window_handles[-1])
#                         time.sleep(2)

#                         try:
#                             WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                             )
#                             description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                         except:
#                             description = ""

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])

#                         skills = extract_flat_skills(description, skill_list)


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
#                         jobs.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing card: {e}")
#                         traceback.print_exc()
#                         continue
#     finally:
#         driver.quit()
#         return jobs

# def main():
#     print("📡 CareerBuilder Crawler Starting…")
#     jobs = get_jobs_from_careerbuilder()
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")

#     write_jobs_csv(jobs, folder_name="debugged", label="careerbuilder")
#     print("🔁 Ensuring database is synced with CSV...")
#     sync_job_data_folder_to_supabase(folder="server/job_data")
#     cleanup(MAX_DAYS)

# if __name__ == "__main__":
#     main()

# import json
# import os
# import time
# import uuid
# import random
# import csv
# import traceback
# from datetime import datetime, timedelta
# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.services.skills import extract_skills
# from app.services.supabase_client import load_skill_matrix
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from app.utils.write_jobs import write_jobs_csv
# from app.services.skills import extract_skills_by_category, load_skill_matrix




# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase



# def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     skills = extract_skills_by_category(description, skill_matrix)
#     jobs = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 try:
#                     driver.get(url)
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Skipping — no job cards found on page {page} for '{keyword}': {e}")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                 for card in cards:
#                     try:
#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                         if not href or href in seen_urls:
#                             continue

#                         seen_urls.add(href)
#                         job_url = href if href.startswith("http") else base_url + href

#                         # 🔁 Tab cleanup: avoid driver crash
#                         if len(driver.window_handles) > 3:
#                             for handle in driver.window_handles[1:]:
#                                 try:
#                                     driver.switch_to.window(handle)
#                                     driver.close()
#                                 except:
#                                     continue
#                             driver.switch_to.window(driver.window_handles[0])

#                         driver.execute_script("window.open(arguments[0])", job_url)
#                         time.sleep(1)
#                         driver.switch_to.window(driver.window_handles[-1])
#                         time.sleep(2)

#                         try:
#                             WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                             )
#                             description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                         except:
#                             description = ""

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])

#                         skills = extract_skills(description, skill_matrix)

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
#                             "search_term": keyword,
#                             "skills": skills
#                         }

#                         insert_job_to_db(job)
#                         jobs.append(job)

#                     except Exception as e:
#                         print(f"❌ Error parsing card: {e}")
#                         traceback.print_exc()
#                         continue
#     finally:
#         driver.quit()
#         return jobs


# def main():
#     print("📡 CareerBuilder Crawler Starting…")
#     jobs = get_jobs_from_careerbuilder()
#     print(f"\n🗂️ Total jobs collected: {len(jobs)}")

#     write_jobs_csv(jobs, folder_name="debugged", label="careerbuilder")
#     print("🔁 Ensuring database is synced with CSV...")
#     sync_job_data_folder_to_supabase(folder="server/job_data")
#     cleanup(MAX_DAYS)

# if __name__ == "__main__":
#     main()
