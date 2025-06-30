# # # career_scraper.py
# import os, time, uuid, traceback, random
# from datetime import datetime
# from dotenv import load_dotenv

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import InvalidSessionIdException

# from app.db.sync_jobs import insert_job_to_db
# from app.db.cleanup import cleanup
# from app.utils.common import TECH_KEYWORDS, LOCATION, PAGES_PER_KEYWORD, MAX_DAYS, configure_driver
# from app.utils.file_helpers import write_jobs_to_csv

# # Load environment
# load_dotenv()
# if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_ANON_KEY"):
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file")


# def is_cloudflare_blocked(driver):
#     return "Cloudflare" in driver.page_source or "Ray ID" in driver.page_source or "Just a moment..." in driver.page_source


# def scrape_careerbuilder(location: str = LOCATION, pages: int = PAGES_PER_KEYWORD, days: int = MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     collected = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 search_url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 try:
#                     if not driver.session_id:
#                         print("⚠️ Driver session lost. Aborting search loop.")
#                         break

#                     driver.get(search_url)
#                     time.sleep(random.uniform(2.5, 5.5))

#                     if is_cloudflare_blocked(driver):
#                         print("🛑 Cloudflare block detected on search page.")
#                         break

#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                     cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                     print(f"📄 Found {len(cards)} cards")

#                     for card in cards:
#                         try:
#                             if not driver.session_id:
#                                 print("🔥 WebDriver session expired.")
#                                 break

#                             title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                             spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                             company = spans[0].text.strip() if spans else "N/A"
#                             job_location = spans[1].text.strip() if len(spans) > 1 else location
#                             job_state = job_location.lower()

#                             href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                             if not href or href in seen_urls:
#                                 continue
#                             seen_urls.add(href)

#                             job_url = href if href.startswith("http") else base_url + href

#                             # Open job page
#                             driver.execute_script("window.open(arguments[0])", job_url)
#                             time.sleep(2)
#                             driver.switch_to.window(driver.window_handles[-1])
#                             time.sleep(2)

#                             if is_cloudflare_blocked(driver):
#                                 print(f"🧱 Blocked on job page: {job_url}")
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
#                                 continue

#                             try:
#                                 WebDriverWait(driver, 6).until(
#                                     EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                                 )
#                                 description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                             except:
#                                 description = ""

#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])

#                             job = {
#                                 "id": str(uuid.uuid4()),
#                                 "title": title,
#                                 "company": company,
#                                 "job_location": job_location,
#                                 "job_state": job_state,
#                                 "date": datetime.today().date(),
#                                 "site": "CareerBuilder",
#                                 "job_description": description,
#                                 "salary": "N/A",
#                                 "url": job_url,
#                                 "applied": False,
#                                 "search_term": keyword,
#                                 "skills": [],
#                                 "skills_by_category": {},
#                                 "priority": 0,
#                                 "status": "new",
#                                 "inserted_at": datetime.utcnow().isoformat(),
#                                 "last_verified": None,
#                                 "user_id": None
#                             }

#                             insert_job_to_db(job)
#                             collected.append(job)

#                         except InvalidSessionIdException:
#                             print("💥 WebDriver crashed mid-card.")
#                             break
#                         except Exception as e:
#                             print(f"❌ Error parsing card: {e}")
#                             traceback.print_exc()
#                             continue

#                 except Exception as e:
#                     print(f"⚠️ Error loading search page {page} for '{keyword}': {e}")
#                     continue

#     finally:
#         try:
#             driver.quit()
#         except:
#             pass
#         if collected:
#             write_jobs_to_csv(collected, prefix="careerbuilderjobs")
#         cleanup(days)

#     return collected



import os, time, uuid, traceback, random
from datetime import datetime
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException

from app.db.sync_jobs import insert_job_to_db
from app.db.cleanup import cleanup
from app.utils.common import TECH_KEYWORDS, LOCATION, PAGES_PER_KEYWORD, MAX_DAYS, configure_driver
from app.utils.file_helpers import write_jobs_to_csv
from app.services.skills_loader import load_all_skills
from app.services.skills import extract_skills_by_category, extract_skills
from app.utils.skill_utils import extract_flat_skills

# Load environment
load_dotenv()
if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_ANON_KEY"):
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file")

SKILLS = load_all_skills()  # 🔁 Unified skill loader

def is_cloudflare_blocked(driver):
    return "Cloudflare" in driver.page_source or "Ray ID" in driver.page_source or "Just a moment..." in driver.page_source

def scrape_careerbuilder(location: str = LOCATION, pages: int = PAGES_PER_KEYWORD, days: int = MAX_DAYS):
    base_url = "https://www.careerbuilder.com"
    driver = configure_driver()
    collected = []
    seen_urls = set()

    try:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 Searching '{keyword}' in '{location}'")
            for page in range(1, pages + 1):
                search_url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

                try:
                    if not driver.session_id:
                        print("⚠️ Driver session lost. Aborting search loop.")
                        break

                    driver.get(search_url)
                    time.sleep(random.uniform(2.5, 5.5))

                    if is_cloudflare_blocked(driver):
                        print("🛑 Cloudflare block detected on search page.")
                        break

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
                    )
                    cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
                    print(f"📄 Found {len(cards)} cards")

                    for card in cards:
                        try:
                            if not driver.session_id:
                                print("🔥 WebDriver session expired.")
                                break

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

                            # Open job page
                            driver.execute_script("window.open(arguments[0])", job_url)
                            time.sleep(2)
                            driver.switch_to.window(driver.window_handles[-1])
                            time.sleep(2)

                            if is_cloudflare_blocked(driver):
                                print(f"🧱 Blocked on job page: {job_url}")
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                                continue

                            try:
                                WebDriverWait(driver, 6).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
                                )
                                description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
                            except:
                                description = ""

                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])

                            flat_skills = extract_flat_skills(description, SKILLS["flat"])
                            categorized_skills = extract_skills_by_category(description, SKILLS["matrix"])

                            job = {
                                "id": str(uuid.uuid4()),
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
                                "skills": flat_skills,
                                "skills_by_category": categorized_skills,
                                "priority": 0,
                                "status": "new",
                                "inserted_at": datetime.utcnow().isoformat(),
                                "last_verified": None,
                                "user_id": None
                            }

                            insert_job_to_db(job)
                            collected.append(job)

                        except InvalidSessionIdException:
                            print("💥 WebDriver crashed mid-card.")
                            break
                        except Exception as e:
                            print(f"❌ Error parsing card: {e}")
                            traceback.print_exc()
                            continue

                except Exception as e:
                    print(f"⚠️ Error loading search page {page} for '{keyword}': {e}")
                    continue

    finally:
        try: driver.quit()
        except: pass
        if collected:
            write_jobs_to_csv(collected, prefix="careerbuilderjobs")
        cleanup(days)

    return collected
# import os, time, uuid, random, traceback
# from datetime import datetime
# from dotenv import load_dotenv

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import InvalidSessionIdException

# from app.db.sync_jobs import insert_job_to_db
# from app.db.cleanup import cleanup
# from app.utils.common import TECH_KEYWORDS, LOCATION, PAGES_PER_KEYWORD, MAX_DAYS, configure_driver
# from app.utils.file_helpers import write_jobs_to_csv
# from app.services.skills import load_skill_matrix, extract_skills

# # Load environment
# load_dotenv()
# if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_ANON_KEY"):
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file")

# def is_cloudflare_blocked(driver):
#     return "Cloudflare" in driver.page_source or "Ray ID" in driver.page_source or "Just a moment..." in driver.page_source

# def scrape_careerbuilder(location: str = LOCATION, pages: int = PAGES_PER_KEYWORD, days: int = MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     skill_matrix = load_skill_matrix()
#     collected = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 search_url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 try:
#                     if not driver.session_id:
#                         print("⚠️ Driver session lost. Aborting search loop.")
#                         break

#                     driver.get(search_url)
#                     time.sleep(random.uniform(2.5, 5.5))

#                     if is_cloudflare_blocked(driver):
#                         print("🛑 Cloudflare block detected on search page.")
#                         break

#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                     cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                     print(f"📄 Found {len(cards)} cards")

#                     for card in cards:
#                         try:
#                             if not driver.session_id:
#                                 print("🔥 WebDriver session expired.")
#                                 break

#                             title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                             spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                             company = spans[0].text.strip() if spans else "N/A"
#                             job_location = spans[1].text.strip() if len(spans) > 1 else location
#                             job_state = job_location.lower()

#                             href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                             if not href or href in seen_urls:
#                                 continue
#                             seen_urls.add(href)

#                             job_url = href if href.startswith("http") else base_url + href

#                             # Open job page
#                             driver.execute_script("window.open(arguments[0])", job_url)
#                             time.sleep(2)
#                             driver.switch_to.window(driver.window_handles[-1])
#                             time.sleep(2)

#                             if is_cloudflare_blocked(driver):
#                                 print(f"🧱 Blocked on job page: {job_url}")
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
#                                 continue

#                             try:
#                                 WebDriverWait(driver, 6).until(
#                                     EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                                 )
#                                 description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                             except:
#                                 description = ""

#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])

#                             skills = extract_skills(description, skill_matrix)
#                             job = {
#                                 "id": str(uuid.uuid4()),
#                                 "title": title,
#                                 "company": company,
#                                 "job_location": job_location,
#                                 "job_state": job_state,
#                                 "date": datetime.today().date(),
#                                 "site": "CareerBuilder",
#                                 "job_description": description,
#                                 "salary": "N/A",
#                                 "url": job_url,
#                                 "applied": False,
#                                 "search_term": keyword,
#                                 "skills": skills,
#                                 "priority": 0,
#                                 "status": "new",
#                                 "inserted_at": datetime.utcnow().isoformat(),
#                                 "last_verified": None,
#                                 "user_id": None
#                             }

#                             insert_job_to_db(job)
#                             collected.append(job)

#                         except InvalidSessionIdException:
#                             print("💥 WebDriver crashed mid-card.")
#                             break
#                         except Exception as e:
#                             print(f"❌ Error parsing card: {e}")
#                             traceback.print_exc()
#                             continue

#                 except Exception as e:
#                     print(f"⚠️ Error loading search page {page} for '{keyword}': {e}")
#                     continue

#     finally:
#         try:
#             driver.quit()
#         except:
#             pass
#         if collected:
#             write_jobs_to_csv(collected, prefix="careerbuilderjobs")
#         cleanup(days)

#     return collected
# # career_scraper.py

# import os
# import time
# import uuid
# import random
# import traceback
# from datetime import datetime
# from dotenv import load_dotenv

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import InvalidSessionIdException

# from app.db.sync_jobs import insert_job_to_db
# from app.db.cleanup import cleanup
# from app.utils.common import TECH_KEYWORDS, LOCATION, PAGES_PER_KEYWORD, MAX_DAYS, configure_driver
# from app.utils.file_helpers import write_jobs_to_csv
# from app.services.skills import load_skill_matrix, extract_skills

# # Load environment variables
# load_dotenv()
# if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_ANON_KEY"):
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file")

# def is_cloudflare_blocked(driver):
#     return "Ray ID" in driver.page_source or "Cloudflare" in driver.page_source or "Just a moment..." in driver.page_source

# def scrape_careerbuilder(location: str = LOCATION, pages: int = PAGES_PER_KEYWORD, days: int = MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     skill_matrix = load_skill_matrix()
#     collected = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 search_url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"
#                 try:
#                     driver.get(search_url)
#                     time.sleep(random.uniform(2.5, 5.5))

#                     if is_cloudflare_blocked(driver):
#                         print("🛑 Cloudflare block detected on search page.")
#                         break

#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )

#                     cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                     print(f"📄 Found {len(cards)} cards")

#                     for card in cards:
#                         try:
#                             if not driver.session_id:
#                                 print("🔥 WebDriver session invalid — skipping.")
#                                 break

#                             title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                             spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                             company = spans[0].text.strip() if spans else "N/A"
#                             job_location = spans[1].text.strip() if len(spans) > 1 else location
#                             job_state = job_location.lower()

#                             href = card.find_element(By.CSS_SELECTOR, "a.job-listing-item").get_attribute("href") or ""
#                             if not href or href in seen_urls:
#                                 continue
#                             seen_urls.add(href)

#                             job_url = href if href.startswith("http") else base_url + href

#                             # Handle tab overflow
#                             while len(driver.window_handles) > 3:
#                                 for h in driver.window_handles[1:]:
#                                     try:
#                                         driver.switch_to.window(h)
#                                         driver.close()
#                                     except:
#                                         pass
#                                 driver.switch_to.window(driver.window_handles[0])

#                             driver.execute_script("window.open(arguments[0])", job_url)
#                             time.sleep(random.uniform(2, 3.5))
#                             driver.switch_to.window(driver.window_handles[-1])
#                             time.sleep(random.uniform(1.5, 2.5))

#                             if is_cloudflare_blocked(driver):
#                                 print(f"🧱 Blocked on job page: {job_url}")
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
#                                 continue

#                             try:
#                                 WebDriverWait(driver, 6).until(
#                                     EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                                 )
#                                 description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                             except:
#                                 description = ""

#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])

#                             skills = extract_skills(description, skill_matrix)
#                             job = {
#                                 "id": str(uuid.uuid4()),
#                                 "title": title,
#                                 "company": company,
#                                 "job_location": job_location,
#                                 "job_state": job_state,
#                                 "date": datetime.today().date(),
#                                 "site": "CareerBuilder",
#                                 "job_description": description,
#                                 "salary": "N/A",
#                                 "url": job_url,
#                                 "applied": False,
#                                 "search_term": keyword,
#                                 "skills": skills,
#                                 "priority": 0,
#                                 "status": "new",
#                                 "inserted_at": datetime.utcnow().isoformat(),
#                                 "last_verified": None,
#                                 "user_id": None
#                             }

#                             insert_job_to_db(job)
#                             collected.append(job)

#                         except InvalidSessionIdException:
#                             print("🔥 WebDriver session crashed mid-loop.")
#                             break
#                         except Exception as e:
#                             print("❌ Error parsing job card:", e)
#                             traceback.print_exc()
#                             continue

#                 except Exception as e:
#                     print(f"⚠️ Skipping page {page} for '{keyword}': {e}")
#                     continue

#     finally:
#         driver.quit()
#         if collected:
#             write_jobs_to_csv(collected, prefix="careerbuilderjobs")
#         cleanup(days)

#     return collected









# import os
# import time
# import uuid
# import json
# import random
# import traceback
# from datetime import datetime
# from dotenv import load_dotenv

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import InvalidSessionIdException



# from app.db.connect_database import get_db_connection
# from app.db.cleanup import cleanup
# from app.db.sync_jobs import insert_job_to_db
# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.utils.file_helpers import write_jobs_to_csv
# from app.services.skills import load_skill_matrix, extract_skills  # or extract_flat_skills


# # ⏬ ENV setup
# load_dotenv()
# if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_ANON_KEY"):
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file")


# # 📡 Entry Point
# def scrape_careerbuilder(location: str = LOCATION, pages: int = PAGES_PER_KEYWORD, days: int = MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     skill_matrix = load_skill_matrix()
#     collected = []

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 search_url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 try:
#                     driver.get(search_url)
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Skipping page {page} for '{keyword}': {e}")
#                     break

#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                 print(f"📄 Found {len(cards)} cards")

#         for card in cards:
#             try:
#                 # ✨ Check if session is valid early
#                 if not driver.session_id:
#                     print("🔥 WebDriver session invalid — skipping.")
#                     break

#                 title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                 spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                 company = spans[0].text.strip() if spans else "N/A"
#                 job_location = spans[1].text.strip() if len(spans) > 1 else location
#                 job_state = job_location.lower()

#                 link = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
#                 href = link.get_attribute("href") or ""
#                 if not href:
#                     continue

#                 job_url = href if href.startswith("http") else base_url + href

#                 # 🚪 Clean up extra tabs
#                 while len(driver.window_handles) > 3:
#                     for h in driver.window_handles[1:]:
#                         try:
#                             driver.switch_to.window(h)
#                             driver.close()
#                         except Exception:
#                             pass
#                     driver.switch_to.window(driver.window_handles[0])

#                 driver.execute_script("window.open(arguments[0])", job_url)
#                 time.sleep(1)
#                 driver.switch_to.window(driver.window_handles[-1])
#                 time.sleep(2)

#                 try:
#                     WebDriverWait(driver, 7).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                     )
#                     description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                 except Exception:
#                     description = ""

#                 driver.close()
#                 driver.switch_to.window(driver.window_handles[0])

#                 skills = extract_skills(description, skill_matrix)

#                 job = {
#                     "id": str(uuid.uuid4()),
#                     "title": title,
#                     "company": company,
#                     "job_location": job_location,
#                     "job_state": job_state,
#                     "date": datetime.today().date(),
#                     "site": "CareerBuilder",
#                     "job_description": description,
#                     "salary": "N/A",
#                     "url": job_url,
#                     "applied": False,
#                     "search_term": keyword,
#                     "skills": skills,
#                     "priority": 0,
#                     "status": "new",
#                     "inserted_at": datetime.utcnow().isoformat(),
#                 }
#                 collected.append(job)
#                 insert_job_to_db(job)

#             except InvalidSessionIdException:
#                 print("🔥 WebDriver session crashed mid-loop.")
#                 break

#             except Exception as e:
#                 print("❌ Error parsing job card:", e)
#                 traceback.print_exc()
#                 continue

#     finally:
#         driver.quit()
#         if collected:
#             write_jobs_to_csv(collected, prefix="careerbuilderjobs")
#         cleanup(days)

#     return collected



# import json
# import sys
# import time
# import uuid
# import json
# import random
# import traceback
# import os
# from datetime import datetime
# from dotenv import load_dotenv
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.utils.file_helpers import write_jobs_to_csv
# from app.db.cleanup import cleanup
# from app.db.connect_database import get_db_connection
# from app.services.skills import extract_skills  # ← Make sure this is present
# from app.services.skills import load_skill_matrix, extract_skills_by_category
# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.services.skills import load_skill_matrix, extract_skills



# load_dotenv()
# url = os.getenv("SUPABASE_URL")
# key = os.getenv("SUPABASE_ANON_KEY")
# if not url or not key:
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
# skill_matrix = load_skill_matrix()
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
#     driver = configure_driver()
#     skill_matrix = load_skill_matrix()
#     career_jobs_scraped = []

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
#                 try:
#                     driver.get(search_url)
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Failed to load page or locate cards for '{keyword}', page {page}: {e}")
#                     break

#                 time.sleep(random.uniform(1.0, 2.0))
#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                 print(f"🧾 Found {len(cards)} cards (page {page})")

#                 for card in cards:
#                     try:
#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         link = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
#                         href = link.get_attribute("href") or ""
#                         if not href:
#                             continue
#                         job_url = href if href.startswith("http") else base_url + href

#                         # Tab overflow management
#                         if len(driver.window_handles) > 3:
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
#                             WebDriverWait(driver, 7).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                             )
#                             description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                         except:
#                             description = ""

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])

#                         skills = extract_skills(description, skill_matrix)

#                         job = {
#                             "title":           title,
#                             "company":         company,
#                             "job_location":    job_location,
#                             "job_state":       job_state,
#                             "date":            datetime.today().date(),
#                             "site":            "CareerBuilder",
#                             "job_description": description,
#                             "salary":          "N/A",
#                             "url":             job_url,
#                             "applied":         False,
#                             "search_term":     keyword,
#                             "skills":          skills,
#                             "priority":        0,
#                             "status":          "new"
#                         }

#                         career_jobs_scraped.append(job)
#                         insert_job_to_db(job)

#                     except Exception as e:
#                         print("❌ Error parsing card:", e)
#                         traceback.print_exc()
#                         continue

#     finally:
#         driver.quit()
#         if career_jobs_scraped:
#             write_jobs_to_csv(career_jobs_scraped, prefix="careerbuilderjobs")
#         cleanup(days)

#     return career_jobs_scraped

# import json
# import sys
# import time
# import uuid
# import json
# import random
# import traceback
# import os
# from datetime import datetime
# from dotenv import load_dotenv
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.utils.file_helpers import write_jobs_to_csv
# from app.db.cleanup import cleanup
# from app.db.connect_database import get_db_connection
# from app.services.skills import extract_skills  # ← Make sure this is present
# from app.services.supabase_client import load_skill_matrix
# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from app.db.sync_jobs import insert_job_to_db, sync_job_data_folder_to_supabase
# from app.services.skills import load_skill_matrix, extract_skills



# load_dotenv()
# url = os.getenv("SUPABASE_URL")
# key = os.getenv("SUPABASE_ANON_KEY")
# if not url or not key:
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

# skills = extract_skills(full_desc, skill_matrix)
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
#     driver = configure_driver()
#     skill_matrix = load_skill_matrix()
#     career_jobs_scraped = []

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
#                 try:
#                     driver.get(search_url)
#                     WebDriverWait(driver, 15).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Failed to load page or locate cards for '{keyword}', page {page}: {e}")
#                     break

#                 time.sleep(random.uniform(1.0, 2.0))
#                 cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                 print(f"🧾 Found {len(cards)} cards (page {page})")

#                 for card in cards:
#                     try:
#                         title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                         spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                         company = spans[0].text.strip() if spans else "N/A"
#                         job_location = spans[1].text.strip() if len(spans) > 1 else location
#                         job_state = job_location.lower()

#                         link = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
#                         href = link.get_attribute("href") or ""
#                         if not href:
#                             continue
#                         job_url = href if href.startswith("http") else base_url + href

#                         # Tab overflow management
#                         if len(driver.window_handles) > 3:
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
#                             WebDriverWait(driver, 7).until(
#                                 EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                             )
#                             description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                         except:
#                             description = ""

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])

#                         skills = extract_skills(description, skill_matrix)

#                         job = {
#                             "title":           title,
#                             "company":         company,
#                             "job_location":    job_location,
#                             "job_state":       job_state,
#                             "date":            datetime.today().date(),
#                             "site":            "CareerBuilder",
#                             "job_description": description,
#                             "salary":          "N/A",
#                             "url":             job_url,
#                             "applied":         False,
#                             "search_term":     keyword,
#                             "skills":          skills,
#                             "priority":        0,
#                             "status":          "new"
#                         }

#                         career_jobs_scraped.append(job)
#                         insert_job_to_db(job)

#                     except Exception as e:
#                         print("❌ Error parsing card:", e)
#                         traceback.print_exc()
#                         continue

#     finally:
#         driver.quit()
#         if career_jobs_scraped:
#             write_jobs_to_csv(career_jobs_scraped, prefix="careerbuilderjobs")
#         cleanup(days)

#     return career_jobs_scraped

# import os
# import time
# import uuid
# import random
# import traceback
# from datetime import datetime
# from dotenv import load_dotenv

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import InvalidSessionIdException

# from app.db.sync_jobs import insert_job_to_db
# from app.db.cleanup import cleanup
# from app.utils.common import (
#     TECH_KEYWORDS,
#     LOCATION,
#     PAGES_PER_KEYWORD,
#     MAX_DAYS,
#     configure_driver
# )
# from app.utils.file_helpers import write_jobs_to_csv
# from app.services.skills import load_skill_matrix, extract_skills

# # ⏬ ENV setup
# load_dotenv()
# if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_ANON_KEY"):
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file")

# # 🌐 Detect Cloudflare block by page content
# def is_cloudflare_blocked(driver):
#     return "Ray ID" in driver.page_source or "Cloudflare" in driver.page_source or "Just a moment..." in driver.page_source

# # 📡 Entry Point
# def scrape_careerbuilder(location: str = LOCATION, pages: int = PAGES_PER_KEYWORD, days: int = MAX_DAYS):
#     base_url = "https://www.careerbuilder.com"
#     driver = configure_driver()
#     skill_matrix = load_skill_matrix()
#     collected = []
#     seen_urls = set()

#     try:
#         for keyword in TECH_KEYWORDS:
#             print(f"\n🔍 Searching '{keyword}' in '{location}'")
#             for page in range(1, pages + 1):
#                 search_url = f"{base_url}/jobs?keywords={'+'.join(keyword.split())}&location={location}&page_number={page}"

#                 try:
#                     driver.get(search_url)
#                     time.sleep(random.uniform(2.5, 5.5))

#                     if is_cloudflare_blocked(driver):
#                         print("🛑 Cloudflare block detected on search page.")
#                         break

#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "li.data-results-content-parent"))
#                     )

#                     cards = driver.find_elements(By.CSS_SELECTOR, "li.data-results-content-parent")
#                     print(f"📄 Found {len(cards)} cards")

#                     for card in cards:
#                         try:
#                             if not driver.session_id:
#                                 print("🔥 WebDriver session invalid — skipping.")
#                                 break

#                             title = card.find_element(By.CSS_SELECTOR, ".data-results-title").text.strip()
#                             spans = card.find_elements(By.CSS_SELECTOR, ".data-details span")
#                             company = spans[0].text.strip() if spans else "N/A"
#                             job_location = spans[1].text.strip() if len(spans) > 1 else location
#                             job_state = job_location.lower()

#                             link = card.find_element(By.CSS_SELECTOR, "a.job-listing-item")
#                             href = link.get_attribute("href") or ""
#                             if not href or href in seen_urls:
#                                 continue

#                             seen_urls.add(href)
#                             job_url = href if href.startswith("http") else base_url + href

#                             # 🚪 Clean up tabs
#                             while len(driver.window_handles) > 3:
#                                 for h in driver.window_handles[1:]:
#                                     try:
#                                         driver.switch_to.window(h)
#                                         driver.close()
#                                     except:
#                                         pass
#                                 driver.switch_to.window(driver.window_handles[0])

#                             driver.execute_script("window.open(arguments[0])", job_url)
#                             time.sleep(random.uniform(2.0, 3.5))
#                             driver.switch_to.window(driver.window_handles[-1])
#                             time.sleep(random.uniform(1.5, 3.0))

#                             if is_cloudflare_blocked(driver):
#                                 print(f"🧱 Blocked on job page: {job_url}")
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
#                                 continue

#                             try:
#                                 WebDriverWait(driver, 6).until(
#                                     EC.presence_of_element_located((By.CSS_SELECTOR, "#jdp_description"))
#                                 )
#                                 description = driver.find_element(By.CSS_SELECTOR, "#jdp_description").text.strip()
#                             except Exception:
#                                 description = ""

#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])

#                             skills = extract_skills(description, skill_matrix)

#                             job = {
#                                 "id": str(uuid.uuid4()),
#                                 "title": title,
#                                 "company": company,
#                                 "job_location": job_location,
#                                 "job_state": job_state,
#                                 "date": datetime.today().date(),
#                                 "site": "CareerBuilder",
#                                 "job_description": description,
#                                 "salary": "N/A",
#                                 "url": job_url,
#                                 "applied": False,
#                                 "search_term": keyword,
#                                 "skills": skills,
#                                 "priority": 0,
#                                 "status": "new",
#                                 "inserted_at": datetime.utcnow().isoformat(),
#                                 "last_verified": None,
#                                 "user_id": None
#                             }

#                             insert_job_to_db(job)
#                             collected.append(job)

#                         except InvalidSessionIdException:
#                             print("🔥 WebDriver session crashed mid-loop.")
#                             break
#                         except Exception as e:
#                             print("❌ Error parsing job card:", e)
#                             traceback.print_exc()
#                             continue

#                 except Exception as e:
#                     print(f"⚠️ Skipping page {page} for '{keyword}': {e}")
#                     continue

#     finally:
#         driver.quit()
#         if collected:
#             write_jobs_to_csv(collected, prefix="careerbuilderjobs")
#         cleanup(days)

#     return collected