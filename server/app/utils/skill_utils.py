import re
def load_flat_skills(filepath="resources/skills.txt") -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]


def extract_flat_skills(description: str, skill_list: list[str]) -> list[str]:
    lowered = (description or "").lower()
    found = {
        skill for skill in skill_list
        if re.search(r"\b" + re.escape(skill) + r"\b", lowered)
    }
    return sorted(found)