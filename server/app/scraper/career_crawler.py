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
