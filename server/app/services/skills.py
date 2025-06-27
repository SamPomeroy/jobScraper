# app/services/skills.py
import re

def extract_skills(text: str, skill_set: set) -> list[str]:
    words = set(re.findall(r"\b[a-zA-Z0-9+\-#\.]{2,}\b", text.lower()))
    return sorted(skill for skill in skill_set if skill in words)