import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("SUPABASE_DATABASE")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=10, sslmode="require")
    return conn

def main():
    # Example usage: test the database connection
    try:
        conn = get_db_connection()
        print("Database connection successful.")
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    main()
