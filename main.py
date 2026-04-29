from fastapi import FastAPI, UploadFile, File
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import docx
import os
import json
import shutil

# ---------------- ENV ----------------
load_dotenv(r"C:\Users\hp\ai-career-assistant\.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("DEBUG KEY:", OPENAI_API_KEY)

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found")

# MUST be after env load
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------- APP ----------------
app = FastAPI()

# ---------------- DB ----------------
DATABASE_URL = "sqlite:///./resumes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    extracted_text = Column(Text)

Base.metadata.create_all(bind=engine)

# ---------------- FILE EXTRACTION ----------------
def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return " ".join([p.extract_text() or "" for p in reader.pages])

    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        with open(file_path, "r", errors="ignore") as f:
            return f.read()

# ---------------- AI FUNCTION ----------------
def extract_with_ai(resume_text):
    prompt = f"""
Extract resume data and return ONLY JSON:

{{
  "name": "",
  "email": "",
  "skills": [],
  "experience_summary": "",
  "score": 0,
  "missing_skills": []
}}

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def safe_json(text):
    try:
        return json.loads(text)
    except:
        return {"raw_output": text}

# ---------------- API ----------------
@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):

    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_file(file_location)

    if not extracted_text.strip():
        return {"error": "No text extracted"}

    ai_result = extract_with_ai(extracted_text)
    parsed_result = safe_json(ai_result)

    db = SessionLocal()
    new_resume = Resume(
        filename=file.filename,
        extracted_text=json.dumps(parsed_result)
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    db.close()

    os.remove(file_location)

    return {
        "message": "Success",
        "data": parsed_result
    }

@app.get("/resumes/")
def get_resumes():
    db = SessionLocal()
    data = db.query(Resume).all()
    db.close()
    return data