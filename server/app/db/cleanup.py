from datetime import datetime
import requests
from app.db.connect_database import get_db_connection

def remove_duplicate_urls():
    """Keep only the newest inserted_at for each URL."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM jobs a
                USING (
                    SELECT url, MAX(inserted_at) AS latest
                    FROM jobs
                    GROUP BY url
                    HAVING COUNT(*) > 1
                ) dups
                WHERE a.url = dups.url
                  AND a.inserted_at < dups.latest;
            """)
        conn.commit()

def purge_older_than(days: int = 15):
    """Remove jobs whose posting date is too old."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM jobs
                WHERE date < CURRENT_DATE - INTERVAL '%s days'
            """, (days,))
        conn.commit()

def is_job_expired(url: str) -> bool:
    """Detect expired job postings based on known phrases."""
    try:
        response = requests.get(url, timeout=10)
        html = response.text.lower()
        expired_keywords = [
            "this job has expired on indeed",
            "not accepting applications",
            "position has been filled",
            "no longer accepting applications",
            "we're sorry"
        ]
        return any(kw in html for kw in expired_keywords)
    except Exception as e:
        print(f"⚠️ Could not verify {url}: {e}")
        return True

def validate_jobs(batch_size: int = 100):
    """Remove expired job URLs using lightweight HTTP check."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, url FROM jobs
                WHERE last_verified IS NULL OR last_verified < NOW() - INTERVAL '7 days'
                LIMIT %s;
            """, (batch_size,))
            jobs = cur.fetchall()

            for job_id, url in jobs:
                if is_job_expired(url):
                    cur.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
                    print(f"🗑️ Deleted expired job: {url}")
                else:
                    cur.execute("UPDATE jobs SET last_verified = %s WHERE id = %s",
                                (datetime.utcnow(), job_id))
        conn.commit()

def cleanup(days: int = 15, validate_batch: int = 100):
    """Run deduplication, pruning, and job validation."""
    print("🧼 Running job cleanup...")
    remove_duplicate_urls()
    purge_older_than(days)
    validate_jobs(validate_batch)
    print("✅ Cleanup complete")