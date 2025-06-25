# db/cleanup.py
from app.db.connect_database import get_db_connection

def remove_duplicate_urls():
    """
    Keep only the newest inserted_at for each URL.
    """
    conn = get_db_connection()
    cur  = conn.cursor()
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
    cur.close()
    conn.close()

def purge_older_than(days: int = 15):
    """
    Remove jobs whose posting date is more than `days` ago.
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute("""
      DELETE FROM jobs
      WHERE date < CURRENT_DATE - INTERVAL '%s days'
    """, (days,))
    conn.commit()
    cur.close()
    conn.close()

def cleanup(days: int = 15):
    remove_duplicate_urls()
    purge_older_than(days)