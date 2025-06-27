import re

def extract_skills(description: str, skill_matrix: list[dict]) -> list[str]:
    """
    Scan job description against your Supabase skill_matrix:
    [ { category: str, skills: [str,...] }, ... ]
    and return a deduped list of matched skills.
    """
    found = set()
    text = (description or "").lower()
    for bucket in skill_matrix:
        for skill in bucket.get("skills", []):
            if skill.lower() in text:
                found.add(skill)
    return sorted(found)