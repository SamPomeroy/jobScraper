# app/scraper/career_crawl4ai.py

import uuid
from datetime import datetime
from urllib.parse import urlencode

import httpx
from selectolax.parser import HTMLParser

from app.utils.common import TECH_KEYWORDS, LOCATION, PAGES_PER_KEYWORD, MAX_DAYS
from app.utils.skill_utils import load_flat_skills, extract_flat_skills
from app.utils.write_jobs import write_jobs_csv
from app.db.sync_jobs import insert_job_to_db
from app.db.cleanup import cleanup

BASE_URL = "https://www.careerbuilder.com"
skill_list = load_flat_skills("app/resources/skills.txt")


def build_url(keyword: str, location: str, page: int) -> str:
    params = {
        "keywords": keyword,
        "location": location,
        "page_number": page
    }
    return f"{BASE_URL}/jobs?{urlencode(params)}"


def get_jobs_from_careerbuilder(location=LOCATION, pages=PAGES_PER_KEYWORD, days=MAX_DAYS):
    print("⚡ Starting fast CareerBuilder crawl...")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    seen_urls = set()
    collected = []

    with httpx.Client(headers=headers, timeout=10) as client:
        for keyword in TECH_KEYWORDS:
            print(f"\n🔍 Keyword: '{keyword}'")
            for page in range(1, pages + 1):
                try:
                    url = build_url(keyword, location, page)
                    response = client.get(url)
                    if response.status_code != 200:
                        print(f"❌ Skipping {url} (status {response.status_code})")
                        continue

                    tree = HTMLParser(response.text)
                    cards = tree.css("li.data-results-content-parent")
                    print(f"📄 Page {page}: Found {len(cards)} job cards")

                    for card in cards:
                        try:
                            anchor = card.css_first("a.job-listing-item")
                            href = (anchor.attributes.get("href") or "").strip() if anchor else ""
                            if not href:
                                continue

                            job_url = href if href.startswith("http") else BASE_URL + href
                            if job_url in seen_urls:
                                continue
                            seen_urls.add(job_url)

                            title = card.css_first(".data-results-title")
                            title_text = title.text(strip=True) if title else "Untitled"

                            spans = card.css(".data-details span")
                            company = spans[0].text(strip=True) if len(spans) > 0 else "N/A"
                            job_location = spans[1].text(strip=True) if len(spans) > 1 else location
                            job_state = job_location.lower()

                            skills = extract_flat_skills(title_text, skill_list)

                            job = {
                                "id": str(uuid.uuid4()),
                                "title": title_text,
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
                                "skills": skills,
                                "priority": 0,
                                "status": "new",
                                "category": None,
                                "inserted_at": datetime.utcnow(),
                                "last_verified": None,
                                "user_id": None
                            }

                            insert_job_to_db(job)
                            collected.append(job)

                        except Exception as e:
                            print(f"⚠️ Error parsing card: {e}")
                            continue

                except Exception as e:
                    print(f"❌ Failed to process page {page} for '{keyword}': {e}")
                    continue

    if collected:
        write_jobs_csv(collected, folder_name="job_data", label="careerbuilder_crawl4ai")
        cleanup(days)

    return collected


def main():
    jobs = get_jobs_from_careerbuilder()
    print(f"\n✅ Collected {len(jobs)} CareerBuilder jobs.")


if __name__ == "__main__":
    main()