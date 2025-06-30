from fastapi import APIRouter
from pydantic import BaseModel
from app.services.skills import load_skill_matrix, extract_skills_by_category

router = APIRouter()

class JobPayload(BaseModel):
    job_description: str

@router.post("/skills/extract")
def extract_from_job(payload: JobPayload):
    job_text = payload.job_description.lower()
    skill_matrix = load_skill_matrix()
    result = extract_skills_by_category(job_text, skill_matrix)
    return {"matched_skills": result}


# # app/api/skill_routes.py
# from fastapi import APIRouter
# from pydantic import BaseModel
# from app.services.skills import load_skill_matrix
# from app.services.skills import extract_skills

# router = APIRouter()
# SKILL_MATRIX = load_skill_matrix()

# class JobPayload(BaseModel):
#     job_description: str

# @router.post("/skills/extract")
# def extract_from_job(payload: JobPayload):
#     job_text = payload.job_description.lower()
#     result = {}

#     for section in SKILL_MATRIX:
#         matched = extract_skills(job_text, set(map(str.lower, section["skills"])))
#         if matched:
#             result[section["category"]] = matched

#     return {"matched_skills": result}