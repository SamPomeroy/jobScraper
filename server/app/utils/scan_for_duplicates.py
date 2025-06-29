from app.db.connect_database import get_db_connection

def scan_for_duplicates():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT url, COUNT(*) as count
        FROM jobs
        GROUP BY url
        HAVING COUNT(*) > 1
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if rows:
        print("🚨 Found duplicate job URLs:")
        for url, count in rows:
            print(f"{url} — {count} times")
    else:
        print("✅ No duplicate job URLs found.")