# modules/agent_logic.py

import pandas as pd
import json
from modules import api_handler

# modules/agent_logic.py

def get_profile_analysis(student_data: dict) -> dict:
    """Analyzes profile and suggests career paths using the Gemini API."""
    prompt = f"""
    You are a career advisor AI for Boston University. Your task is to analyze a student's academic profile and return a JSON object.

    **Student Data:**
    {json.dumps(student_data, indent=2)}

    **Your Instructions:**
    1.  Analyze the student's major and courses to identify 2-3 of their key academic strengths.
    2.  Based on these strengths, suggest exactly two relevant and specific career paths.
    
    **CRITICAL:** You MUST respond with a single, valid JSON object and nothing else. The JSON object must contain two keys: "strengths" (a list of strings) and "suggested_paths" (a list of strings). Both keys are mandatory.

    **Example Format:**
    {{"strengths": ["Strength 1", "Strength 2"], "suggested_paths": ["Career Path 1", "Career Path 2"]}}
    """
    response_dict = api_handler.get_llm_response(prompt)
    return response_dict

def perform_skill_gap_analysis(student_data: dict, user_skills: list, job_title: str, job_requirements: dict) -> dict:
    """Performs a skill-gap analysis by comparing student and user skills to job requirements."""
    student_skills = set(skill for course in student_data.get("courses", []) for skill in course.get("skills", []))
    all_my_skills = student_skills.union(set(user_skills))
    required_skills = set(job_requirements.get(job_title, {}).get("required_skills", []))
    
    skills_have = list(all_my_skills.intersection(required_skills))
    skills_needed = list(required_skills.difference(all_my_skills))
    
    return {"skills_have": skills_have, "skills_needed": skills_needed}

def recommend_courses(skills_needed: list, course_catalog: list) -> list:
    """Recommends specific courses from the catalog to fill skill gaps."""
    recommendations = []
    needed_set = set(skills_needed)
    for course in course_catalog:
        if not needed_set.isdisjoint(set(course.get("provides_skills", []))):
            recommendations.append(course)
    return recommendations

def find_relevant_alumni(job_title: str, alumni_df: pd.DataFrame) -> pd.DataFrame:
    """Finds alumni in the database with a matching job title."""
    return alumni_df[alumni_df['job_title'].str.lower() == job_title.lower()]

