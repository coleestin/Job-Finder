import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

model = "gemini-2.0-flash"

def build_resume_prompt(resume_text: str) -> str:
    return f"""
You are an expert resume parser. Your task is to extract structured information 
from a raw resume text and return it in clean, valid JSON. 

Rules:
- Only include information explicitly present in the resume.
- If a field is missing, return an empty list or empty string.
- Do not invent or infer information.
- Use consistent keys and formatting.

Extract the following fields:

{{
  "name": "Full name of the candidate",
  "contact": {{
    "email": "Email address",
    "phone": "Phone number",
    "linkedin": "LinkedIn URL if present",
    "location": "City, State, Country if present"
  }},
  "summary": "Professional summary or objective statement",
  "skills": ["List of skills, technologies, programming languages, tools"],
  "experience": [
    {{
      "company": "Company name",
      "role": "Job title",
      "start_date": "Start date if available",
      "end_date": "End date or 'Present'",
      "description": "Bulleted or paragraph description of responsibilities/achievements"
    }}
  ],
  "education": [
    {{
      "institution": "School/University name",
      "degree": "Degree earned (B.Sc., M.Sc., etc.)",
      "field_of_study": "Field of study",
      "start_date": "Start date if available",
      "end_date": "End date or graduation year"
    }}
  ],
  "projects": [
    {{
      "title": "Project name",
      "description": "Short description of the project",
      "technologies": ["List of technologies used if available"]
    }}
  ],
  "certifications": [
    {{
      "name": "Certification name",
      "issuer": "Issuing organization",
      "date": "Date issued if available"
    }}
  ]
}}

Now, given the following resume text, return only the JSON:
---
{resume_text}
---
"""

def get_resume_details(resume: str):
    response = client.models.generate_content(
        model=model,
        contents=build_resume_prompt(resume),
        config={
        "response_mime_type": "application/json",
        },
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # If the response is not valid JSON, return a default structure
        return {
            "{ blah: blah }"
        }
