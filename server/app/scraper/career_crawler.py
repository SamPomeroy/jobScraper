# import time
# import random
# from datetime import datetime
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# def get_jobs_from_crawl4ai(location="remote", days=30):
#     print(f"🌐 Scraping Indeed via Crawl4AI for location='{location}'")
#     base_url = "https://www.careerbuilder.com"
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
