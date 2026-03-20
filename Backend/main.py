from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import json
import io
import re
from collections import defaultdict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("courses.json") as f:
    COURSE_CATALOG = json.load(f)

SKILL_ALIASES = {
    "python": "python", "py": "python",
    "javascript": "javascript", "js": "javascript",
    "typescript": "typescript", "ts": "typescript",
    "java": "java", "c++": "c++", "golang": "golang", "go": "golang",
    "ruby": "ruby", "php": "php",
    "react": "react", "reactjs": "react", "react.js": "react",
    "vue": "vue", "angular": "angular",
    "html": "html", "css": "css",
    "frontend": "frontend", "front-end": "frontend",
    "web development": "web development",
    "fastapi": "fastapi", "fast api": "fastapi",
    "django": "django", "flask": "flask",
    "rest api": "rest api", "restful": "rest api", "api": "rest api",
    "backend": "backend", "back-end": "backend",
    "node.js": "node.js", "nodejs": "node.js", "express": "node.js",
    "sql": "sql", "mysql": "sql", "postgresql": "sql", "postgres": "sql",
    "sqlite": "sql", "database": "sql",
    "nosql": "nosql", "mongodb": "nosql",
    "pandas": "pandas", "numpy": "numpy",
    "data analysis": "data analysis", "data analytics": "data analysis",
    "data science": "data science",
    "machine learning": "machine learning", "ml": "machine learning",
    "deep learning": "deep learning",
    "tensorflow": "tensorflow", "pytorch": "pytorch",
    "scikit-learn": "machine learning",
    "power bi": "power bi", "powerbi": "power bi",
    "tableau": "tableau",
    "docker": "docker", "containerization": "docker",
    "kubernetes": "kubernetes", "k8s": "kubernetes",
    "aws": "aws", "amazon web services": "aws",
    "azure": "azure", "gcp": "gcp", "google cloud": "gcp",
    "devops": "devops", "ci/cd": "devops",
    "git": "git", "github": "git", "version control": "git",
    "linux": "linux", "bash": "linux",
    "excel": "excel", "microsoft excel": "excel", "spreadsheet": "excel",
    "microsoft office": "excel",
    "inventory": "inventory management", "inventory management": "inventory management",
    "warehouse": "inventory management", "warehousing": "inventory management",
    "wms": "wms", "warehouse management system": "wms",
    "ims": "wms", "inventory management system": "wms",
    "logistics": "logistics", "supply chain": "supply chain",
    "procurement": "supply chain", "fulfilment": "logistics",
    "forklift": "forklift", "pallet": "forklift",
    "dispatch": "logistics", "inbound": "logistics", "outbound": "logistics",
    "osha": "osha", "safety": "osha", "workplace safety": "osha",
    "fire safety": "osha", "ppe": "osha", "compliance": "osha",
    "leadership": "leadership", "team lead": "leadership",
    "team management": "leadership", "management": "leadership",
    "supervise": "leadership", "supervisor": "leadership",
    "communication": "communication", "presentation": "communication",
    "public speaking": "public speaking",
    "agile": "agile", "scrum": "agile", "kanban": "agile",
    "project management": "project management",
    "time management": "time management",
    "finance": "finance", "budgeting": "finance", "accounting": "finance",
    "hr": "hr", "human resources": "hr", "recruitment": "hr",
    "marketing": "digital marketing", "seo": "digital marketing",
    "digital marketing": "digital marketing",
    "customer service": "customer service", "crm": "customer service",
    "cybersecurity": "cybersecurity", "security": "cybersecurity",
    "testing": "qa", "qa": "qa", "quality assurance": "qa",
}

LEVEL_ORDER = {"beginner": 1, "intermediate": 2, "advanced": 3}


def extract_text(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower().strip()


def extract_skills(text: str) -> set:
    found = set()
    sorted_aliases = sorted(SKILL_ALIASES.keys(), key=len, reverse=True)
    for keyword in sorted_aliases:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text):
            found.add(SKILL_ALIASES[keyword])
    return found


def find_skill_gap(resume_skills: set, jd_skills: set) -> set:
    return jd_skills - resume_skills


def match_courses(skill_gap: set) -> list:
    course_scores = defaultdict(int)
    for skill in skill_gap:
        for course in COURSE_CATALOG:
            for tag in course["skill_tags"]:
                tag_c = SKILL_ALIASES.get(tag.lower(), tag.lower())
                if tag_c == skill or skill in tag_c or tag_c in skill:
                    course_scores[course["id"]] += 1
                    break
    matched = [c for c in COURSE_CATALOG if course_scores[c["id"]] > 0]
    matched.sort(key=lambda c: (LEVEL_ORDER.get(c["level"], 2), -course_scores[c["id"]]))
    return matched


def generate_reason(course: dict, skill_gap: set) -> str:
    matched_gaps = []
    for tag in course["skill_tags"]:
        tag_c = SKILL_ALIASES.get(tag.lower(), tag.lower())
        for gap in skill_gap:
            if tag_c == gap or gap in tag_c or tag_c in gap:
                matched_gaps.append(gap)
                break
    matched_gaps = list(set(matched_gaps))[:3]
    skills_str = ", ".join(matched_gaps) if matched_gaps else "required skills"
    if course["level"] == "beginner":
        return f"Your profile shows no experience in {skills_str} — this beginner course builds the foundation needed for the role."
    elif course["level"] == "intermediate":
        return f"The job requires {skills_str} at a working level — this course closes that gap directly."
    else:
        return f"The role demands advanced {skills_str} skills — this course prepares you for that responsibility."


@app.get("/")
def root():
    return {"status": "PathForge AI is running", "engine": "rule-based skill matcher"}

@app.get("/health")
def health():
    return {"status": "ok", "engine": "rule-based", "courses_loaded": len(COURSE_CATALOG)}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    resume_text = extract_text(await resume.read())
    jd_text     = extract_text(await jd.read())

    if not resume_text:
        return {"error": "Could not read resume PDF."}
    if not jd_text:
        return {"error": "Could not read job description PDF."}

    resume_skills = extract_skills(resume_text)
    jd_skills     = extract_skills(jd_text)
    skill_gap     = find_skill_gap(resume_skills, jd_skills)

    if not skill_gap:
        return {
            "candidate_skills": sorted(resume_skills),
            "required_skills":  sorted(jd_skills),
            "skill_gap":        [],
            "learning_pathway": [],
            "message": "Great news! Your profile already matches the job requirements."
        }

    matched_courses = match_courses(skill_gap)

    pathway = []
    for i, course in enumerate(matched_courses):
        pathway.append({
            "week":         i + 1,
            "course_id":    course["id"],
            "course_title": course["title"],
            "level":        course["level"],
            "duration":     course["duration"],
            "reason":       generate_reason(course, skill_gap)
        })

    return {
        "candidate_skills": sorted(resume_skills),
        "required_skills":  sorted(jd_skills),
        "skill_gap":        sorted(skill_gap),
        "learning_pathway": pathway
    }
