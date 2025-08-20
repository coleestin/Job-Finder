import os
from dotenv import load_dotenv
from supabase import create_client, Client
from supabase.client import ClientOptions


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(
    url,
    key,
    options=ClientOptions()
)

def get_or_create_user(name: str, email: str) -> str | None:
    # Check if user exists
    existing = supabase.table("users").select("id").eq("email", email).execute()
    if existing.data:
        return existing.data[0]["id"]
    
    # Otherwise create new
    response = supabase.table("users").insert({"name": name, "email": email}).execute()
    if response.data:
        return response.data[0]["id"]
    return None

#TODO: add more fields, we want to embed different details (summary, skills, experience, projects) individually
def save_resume(user_id: str, raw_text: str, structured_data: dict, embedding: list[float]):
    response = (
        supabase.table("resumes")
        .insert({
            "user_id": user_id,
            "name": structured_data["name"],
            "contact": structured_data["contact"],
            "summary": structured_data["summary"],
            "skills": structured_data["skills"],
            "experience": structured_data["experience"],
            "education": structured_data["education"],
            "projects": structured_data["projects"],
            "certifications": structured_data["certifications"],
            "embedding": embedding,
            "raw_text" : raw_text
        })
        .execute()
    )




