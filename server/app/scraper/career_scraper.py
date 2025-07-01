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
