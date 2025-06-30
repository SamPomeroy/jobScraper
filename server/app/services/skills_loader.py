# server/app/services/skills_loader.py

from app.services.supabase_client import supabase
from app.utils.skill_utils import load_flat_skills

def load_skill_matrix():
    """Pull categorized skills from Supabase."""
    response = supabase.table("skill_categories").select("*").execute()
    return response.data or []

def load_all_skills():
    """
    Load all skill types into a unified dictionary.
    - flat: simple keyword list from skills.txt
    - matrix: categorized skills from Supabase
    - json: optional future slot
    """
    return {
        "flat": load_flat_skills("app/resources/skills.txt"),
        "matrix": load_skill_matrix(),
        "json": {}  # Placeholder if needed later
    }