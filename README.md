# AI Resume Analyzer API

A FastAPI-powered backend that automatically extracts and analyzes resume data using OpenAI — turning unstructured PDF/DOCX resumes into structured, queryable JSON insights.

---

## What It Does

Upload any resume (PDF or DOCX) and the API will:
- Extract raw text from the document
- Use OpenAI GPT to intelligently parse name, email, skills, and experience
- Score the resume and identify missing skills
- Store results in SQLite for retrieval
- Return clean, structured JSON instantly

---

## Example

**Input:** Upload `swathi_resume.pdf`

**Output:**
```json
{
  "name": "Swathi Datla",
  "email": "datlaswathi67@gmail.com",
  "skills": ["Python", "FastAPI", "React", "Django", "REST APIs", "SQL"],
  "experience_summary": "Master's graduate in Applied Computer Science with hands-on experience in full-stack development and AI-powered applications.",
  "score": 82,
  "missing_skills": ["Docker", "AWS", "Kubernetes"]
}
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| AI / LLM | OpenAI GPT-4o-mini |
| File Parsing | pypdf, python-docx |
| Database | SQLite via SQLAlchemy |
| Server | Uvicorn |
| Config | python-dotenv |

---

## API Endpoints

| Method | Endpoint | Description |

| POST | `/upload-resume/` | Upload a PDF or DOCX resume for AI analysis |
| GET | `/resumes/` | Retrieve all previously analyzed resumes |
| GET | `/docs` | Interactive Swagger UI |

---

## Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/SwathiDatla/ai-career-assistant.git
cd ai-career-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. Start the server
```bash
python -m uvicorn main:app --reload
```

### 5. Test the API

Open your browser and go to:
```
http://127.0.0.1:8000/docs
```

Use the Swagger UI to upload a resume and see the AI extraction in action.

---

## Project Structure

```
ai-career-assistant/
├── main.py           # FastAPI app, routes, AI logic
├── resumes.db        # SQLite database (auto-created)
├── requirements.txt  # Dependencies
├── .env              # API keys (not committed)
└── README.md
```

---

## Requirements

```
fastapi
uvicorn
openai
pypdf
python-docx
sqlalchemy
python-dotenv
python-multipart
```



## Author

**Swathi Datla**  
M.S. Applied Computer Science — Southeast Missouri State University  
[LinkedIn](https://www.linkedin.com/in/swathi-datla) · [GitHub](https://github.com/SwathiDatla)

