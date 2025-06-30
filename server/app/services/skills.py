from app.services.supabase_client import supabase

def load_skill_matrix():
    response = supabase.table("skill_categories").select("*").execute()
    return response.data  # [{ "category": ..., "skills": [...] }]

def extract_skills(description: str, skill_matrix: list[dict]) -> list[str]:
    """Extract a deduplicated list of skills found in the job description."""
    found = set()
    lowered_desc = (description or "").lower()
    for section in skill_matrix:
        for skill in section.get("skills", []):
            if skill.lower() in lowered_desc:
                found.add(skill)
    return sorted(found)


def extract_skills_by_category(description: str, skill_matrix: list[dict]) -> dict:
    """Return a dictionary of matched skills grouped by category."""
    matches = {}
    lowered = (description or "").lower()
    for section in skill_matrix:
        found = [s for s in section.get("skills", []) if s.lower() in lowered]
        if found:
            matches[section["category"]] = found
    return matches