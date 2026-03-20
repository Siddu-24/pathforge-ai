from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import requests
import json
import io

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

# Ollama runs locally — no API key needed
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

def call_ollama(prompt: str) -> str:
    """Send a prompt to local Ollama and return the response text."""
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=120)  # 2 min timeout — local models can be slow
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        raise Exception("Ollama is not running. Please start it with: ollama serve")
    except requests.exceptions.Timeout:
        raise Exception("Ollama took too long to respond. Try again.")
    except Exception as e:
        raise Exception(f"Ollama error: {str(e)}")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF file."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def clean_json(raw: str) -> str:
    """Remove markdown code fences if the model wraps output in them."""
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return raw.strip()

@app.get("/health")
def health_check():
    """Check if backend and Ollama are both running."""
    try:
        requests.get("http://localhost:11434", timeout=5)
        return {"status": "ok", "ollama": "running", "model": OLLAMA_MODEL}
    except:
        return {"status": "ok", "ollama": "NOT running — start with: ollama serve"}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    # Step 1: Extract text from both PDFs
    resume_text = extract_text_from_pdf(await resume.read())
    jd_text = extract_text_from_pdf(await jd.read())

    if not resume_text:
        return {"error": "Could not read resume PDF. Make sure it is not scanned/image-only."}
    if not jd_text:
        return {"error": "Could not read job description PDF."}

    # Step 2: Build the catalog summary to send to the model
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

    # Step 3: Build the prompt
    prompt = f"""You are an expert HR onboarding AI. Your job is to analyze a resume and job description, find the skill gap, and recommend a personalized learning pathway.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

AVAILABLE COURSE CATALOG (you must ONLY recommend courses from this list — do not invent new ones):
{catalog_summary}

Instructions:
1. Extract the candidate's current skills from the resume.
2. Extract the required skills from the job description.
3. Find the skill gap: skills in the JD that are missing from the resume.
4. Recommend courses ONLY from the catalog above that address the skill gap.
5. Order courses: beginner first, advanced last.
6. Assign a week number to each course starting from Week 1.
7. For each course write one sentence explaining why it was chosen.

You MUST respond with ONLY a valid JSON object. No explanation before or after. No markdown. No extra text. Just the raw JSON.

Use exactly this format:
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

    # Step 4: Call local Ollama
    try:
        raw_response = call_ollama(prompt)
    except Exception as e:
        return {"error": str(e)}

    # Step 5: Parse the JSON response
    try:
        cleaned = clean_json(raw_response)
        result = json.loads(cleaned)
        return result
    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON. Raw response below — try again.",
            "raw": raw_response[:1000]
        }