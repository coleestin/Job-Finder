from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import shutil
from uuid import uuid4
import pymupdf
from llm import get_resume_details
from database import get_or_create_user, save_resume

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    user_name: str = Form(...),
    user_email: str = Form(...)
):
    # Generate unique filename
    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    get_or_create_user(user_name,user_email)

    file_bytes = file.read()

    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:  
        text += page.get_text("text")
    doc.close()

    json_details = get_resume_details(text)

    return JSONResponse({
        "status": "success",
        "filename": filename,
        "parsed": json_details
    })
