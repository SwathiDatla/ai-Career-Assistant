from fastapi import FastAPI, UploadFile, File
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"message": "AI Career Assistant Running"}

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text(file, content)

    return {
        "filename": file.filename,
        "extracted_text": text[:1000]  # preview only
    }

def extract_text(file: UploadFile, content: bytes):
    if file.filename.endswith(".docx"):
        from docx import Document
        import io

        doc = Document(io.BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs])

    elif file.filename.endswith(".pdf"):
        from PyPDF2 import PdfReader
        import io

        reader = PdfReader(io.BytesIO(content))
        return "\n".join([page.extract_text() for page in reader.pages])

    return content.decode("utf-8", errors="ignore")