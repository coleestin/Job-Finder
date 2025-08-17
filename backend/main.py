from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import shutil
from uuid import uuid4
import pymupdf
from llm import get_resume_details

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    # Generate unique filename
    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:  
        text += page.get_text("text")  # extract text page by page
    doc.close()

    json_details = get_resume_details(text)

    return JSONResponse({
        "status": "success",
        "filename": filename,
        "parsed": json_details
    })
