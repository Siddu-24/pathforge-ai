from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import google.generativeai as genai
import json
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load course catalog once at startup
with open("courses.json") as f:
    COURSE_CATALOG = json.load(f)

# Gemini setup — API key from environment variable
genai.configure(api_key=os.environ.get("AIzaSyDzakLstBGMqsTybsVIpYUcVEdZ2Gq3dL0"))
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def clean_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return raw.strip()

@app.get("/")
def root():
    return {"status": "PathForge AI backend is running"}

@app.get("/health")
def health():
    return {"status": "ok", "model": "gemini-1.5-flash"}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    resume_text = extract_text_from_pdf(await resume.read())
    jd_text = extract_text_from_pdf(await jd.read())

    if not resume_text:
        return {"error": "Could not read resume PDF."}
    if not jd_text:
        return {"error": "Could not read job description PDF."}

    catalog_summary = json.dumps([
        {
            "id": c["id"],
            "title": c["title"],
            "skill_tags": c["skill_tags"],
            "level": c["level"],
            "duration": c["duration"]
        }
        for c in COURSE_CATALOG
    ])

    prompt = f"""You are an expert HR onboarding AI. Analyze the resume and job description below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

AVAILABLE COURSE CATALOG (ONLY recommend courses from this list):
{catalog_summary}

Instructions:
1. Extract candidate's current skills from resume.
2. Extract required skills from job description.
3. Find skill gap: skills in JD missing from resume.
4. Recommend courses ONLY from catalog that address the skill gap.
5. Order courses: beginner first, advanced last.
6. Assign week numbers starting from Week 1.
7. Write one sentence reason for each course.

Respond ONLY with valid JSON, no extra text, no markdown:
{{
  "candidate_skills": ["skill1", "skill2"],
  "required_skills": ["skill1", "skill2"],
  "skill_gap": ["missing1", "missing2"],
  "learning_pathway": [
    {{
      "week": 1,
      "course_id": 1,
      "course_title": "Exact title from catalog",
      "level": "beginner",
      "duration": "X hours",
      "reason": "One sentence reason why this course was selected."
    }}
  ]
}}"""

    try:
        response = model.generate_content(prompt)
        raw = response.text
        cleaned = clean_json(raw)
        result = json.loads(cleaned)
        return result
    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON. Please try again.",
            "raw": raw[:500]
        }
    except Exception as e:
        return {"error": str(e)}
