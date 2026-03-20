# ⚒️ PathForge AI

> An intelligent onboarding system that parses a new hire's resume and a job description, identifies the skill gap, and dynamically generates a personalized learning roadmap — powered by Claude AI.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [How the Skill-Gap Analysis Works](#how-the-skill-gap-analysis-works)
- [Datasets Used](#datasets-used)
- [Docker (Optional)](#docker-optional)
- [Demo](#demo)

---

## Overview

Traditional corporate onboarding uses a one-size-fits-all approach. Experienced hires waste time on content they already know, while beginners get overwhelmed by advanced modules.

This project solves that problem by:
1. Extracting skills from a candidate's **resume** and a **job description**
2. Identifying the exact **skill gap** between the two
3. Generating a **week-by-week personalized training roadmap** from a grounded course catalog
4. Providing a **reasoning trace** for every course recommendation

---

## Features

- **Intelligent Parsing** — Extracts structured skill lists from resume and JD PDFs using Claude AI
- **Skill Gap Analysis** — Compares candidate skills vs. role requirements and identifies what's missing
- **Adaptive Pathway Generation** — Recommends courses ordered from beginner → advanced using dependency-aware logic
- **Reasoning Trace** — Every course recommendation includes a plain-English explanation of why it was selected
- **Grounded Recommendations** — The AI strictly recommends from a predefined course catalog (zero hallucinations)
- **Cross-Domain Support** — Works for both technical roles (Software Engineer, Data Analyst) and operational roles (Warehouse Manager, HR Associate)
- **Web UI** — Clean, responsive React interface for uploading documents and visualizing the roadmap

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React (Vite) |
| Backend | Python, FastAPI |
| AI Engine | Claude claude-sonnet-4-20250514 (Anthropic API) |
| PDF Parsing | pdfplumber |
| HTTP Client | Axios |
| Skill Taxonomy | O*NET Database, Kaggle Resume Dataset |
| Containerization | Docker (optional) |

---

## Project Structure

```
project/
├── backend/
│   ├── main.py              # FastAPI server — all API logic
│   ├── courses.json         # Grounded course catalog (30 courses)
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   └── App.jsx          # Main React UI component
│   ├── package.json
│   └── vite.config.js
├── Dockerfile               # Optional Docker setup
└── README.md
```

---

## Setup & Installation

### Prerequisites

Make sure you have the following installed:

- [Node.js](https://nodejs.org/) v18 or higher
- [Python](https://python.org/) 3.9 or higher
- An [Anthropic API Key](https://console.anthropic.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-onboarding-engine.git
cd ai-onboarding-engine
```

---

### 2. Backend Setup

```bash
cd backend
pip install fastapi uvicorn pdfplumber anthropic python-multipart
```

Open `main.py` and replace the API key placeholder:

```python
client = anthropic.Anthropic(api_key="YOUR_CLAUDE_API_KEY_HERE")
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm install axios
```

---

## How to Run

You need **two terminals open** at the same time.

**Terminal 1 — Start the Backend:**

```bash
cd backend
uvicorn main:app --reload
```

The backend will run at: `http://localhost:8000`

**Terminal 2 — Start the Frontend:**

```bash
cd frontend
npm run dev
```

The frontend will run at: `http://localhost:5173`

Open `http://localhost:5173` in your browser. Upload a Resume PDF and a Job Description PDF, then click **Generate My Learning Roadmap**.

---

## How the Skill-Gap Analysis Works

The adaptive logic follows three stages:

### Stage 1 — Skill Extraction
The resume and job description PDFs are read using `pdfplumber`. Both texts are sent to the Claude AI model with a structured prompt that instructs it to return a JSON object containing the candidate's current skills and the role's required skills.

### Stage 2 — Gap Identification
The model compares both skill lists and outputs a `skill_gap` array — the set of skills present in the job description but absent or underdeveloped in the resume. This becomes the input for the pathway generator.

### Stage 3 — Adaptive Pathway Generation (Original Logic)
The system generates a learning pathway using a **dependency-aware ordering algorithm**:

- Each course in `courses.json` has a `level` field (`beginner`, `intermediate`, `advanced`) and a `prerequisites` array listing required prior skills.
- The AI model is instructed to recommend only courses from the catalog that address the identified skill gaps.
- Courses are ordered so that foundational (`beginner`) courses always appear before `intermediate` ones, and `intermediate` before `advanced` — mirroring topological sort logic on a skill dependency graph.
- The model assigns a `week` number to each course, producing a sequenced multi-week training plan.
- Every course includes a `reason` field — a one-sentence reasoning trace explaining the selection.

This approach ensures the output is always grounded (no invented courses), logically sequenced, and explainable.

---

## Course Catalog

The `courses.json` file contains **30 pre-defined courses** across 7 domains:

| Domain | Example Courses |
|--------|----------------|
| Technical | Python, SQL, Docker, AWS, React, Machine Learning |
| Management | Agile/Scrum, Leadership, Product Management |
| Operations | Inventory Management, Workplace Safety, Power BI |
| Soft Skills | Business Communication, Time Management, Public Speaking |
| Finance | Financial Reporting & Budgeting |
| Marketing | Digital Marketing Fundamentals |
| HR | HR Fundamentals & People Operations |

The AI model is strictly constrained to recommend only from this catalog, which ensures **zero hallucinations** and consistent, auditable recommendations.

---

## Datasets Used

| Dataset | Usage |
|---------|-------|
| [O*NET Database](https://www.onetcenter.org/db_releases.html) | Skill taxonomy and occupational competency framework used to inform course tagging and skill gap logic |
| [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset/data) | Used to test and validate the resume skill extraction pipeline across diverse role types |
| [Kaggle Jobs & Job Descriptions](https://www.kaggle.com/datasets/kshitizregmi/jobs-and-job-description) | Used to validate JD skill extraction across a range of industries and job levels |

All datasets are publicly available. No proprietary data was used.

---

## Docker (Optional)

To run the backend in a Docker container:

```bash
docker build -t onboarding-engine .
docker run -p 8000:8000 onboarding-engine
```

**Dockerfile:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/ .
RUN pip install fastapi uvicorn pdfplumber anthropic python-multipart
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Demo

Watch the 2-minute demo walkthrough: **[Link to Video]**

The demo shows:
- Uploading a junior developer resume vs. a senior engineer job description
- The skill gap analysis output
- The generated week-by-week roadmap with reasoning traces
- A second test with a non-technical role to demonstrate cross-domain scalability

---

## Evaluation Criteria Coverage

| Criterion | Implementation |
|-----------|---------------|
| Technical Sophistication (20%) | Claude API extracts structured skills; dependency-ordered adaptive pathing |
| Grounding & Reliability (15%) | AI strictly limited to `courses.json` catalog — no hallucinations |
| Reasoning Trace (10%) | Every course has a `reason` field shown in the UI |
| Product Impact (10%) | Eliminates redundant training by targeting only missing skills |
| User Experience (15%) | Clean dark-themed React UI with skill gap cards and roadmap timeline |
| Cross-Domain Scalability (10%) | Catalog covers both tech and non-tech roles |
| Communication & Documentation (20%) | This README + demo video + 5-slide deck |

---

## Team

Built for the **ARTPARK CodeForge Hackathon** — PathForge AI Challenge.

| Name | Role |
|------|------|
| V Girish Siddharth | Frontend Developer |
| Mudusu Sai Haneesha Reddy | Backend Developer |
| T Mokshitha | AI/ML Engineer |
| Veldooti Venkata Sri Harshith | AI/ML Engineer |