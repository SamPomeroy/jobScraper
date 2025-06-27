# services/supabase_client.py
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables must be set")
supabase = create_client(url, key)

def load_skill_matrix():
    response = supabase.table("skill_categories").select("*").execute()
    return response.data  # List of { "category": ..., "skills": [...] }