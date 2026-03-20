import { useState } from "react";

const styles = `
  /* Google Fonts - free, commonly used by students */
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

  /* ── Reset ── */
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  /* ── Root variables ── */
  :root {
    --black:   #0f0f0f;
    --white:   #ffffff;
    --gray-1:  #f4f4f4;
    --gray-2:  #e8e8e8;
    --gray-3:  #aaaaaa;
    --gray-4:  #666666;
    --green:   #1a6b3c;
    --green-bg:#eef7f2;
    --red:     #b03000;
    --red-bg:  #fff3ee;
    --accent:  #1a6b3c;
    --radius:  4px;
    --mono:    'IBM Plex Mono', monospace;
    --sans:    'IBM Plex Sans', sans-serif;
  }

  body {
    font-family: var(--sans);
    background: var(--white);
    color: var(--black);
    font-size: 15px;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
  }

  /* ── Layout ── */
  .page {
    max-width: 780px;
    margin: 0 auto;
    padding: 56px 28px 100px;
  }

  /* ── Top nav bar ── */
  .topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1.5px solid var(--black);
    padding-bottom: 18px;
    margin-bottom: 52px;
  }

  .topbar-left {
    display: flex;
    align-items: baseline;
    gap: 14px;
  }

  .logo {
    font-family: var(--mono);
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -0.3px;
    color: var(--black);
  }

  .logo-dot {
    color: var(--accent);
  }

  .tagline {
    font-size: 12px;
    color: var(--gray-4);
    font-family: var(--mono);
  }

  .version-badge {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--gray-4);
    border: 1px solid var(--gray-2);
    padding: 3px 8px;
    border-radius: var(--radius);
  }

  /* ── Intro block ── */
  .intro {
    margin-bottom: 40px;
  }

  .intro h1 {
    font-family: var(--sans);
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.5px;
    line-height: 1.25;
    margin-bottom: 10px;
    color: var(--black);
  }

  .intro p {
    font-size: 14px;
    color: var(--gray-4);
    max-width: 520px;
    line-height: 1.7;
  }

  /* ── Label style ── */
  .label {
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--gray-4);
    margin-bottom: 10px;
    display: block;
  }

  /* ── Upload section ── */
  .upload-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 14px;
  }

  @media (max-width: 560px) {
    .upload-grid { grid-template-columns: 1fr; }
  }

  .upload-card {
    position: relative;
    border: 1.5px solid var(--gray-2);
    border-radius: var(--radius);
    padding: 22px 20px;
    cursor: pointer;
    background: var(--white);
    transition: border-color 0.2s ease, background 0.2s ease;
  }

  .upload-card:hover {
    border-color: var(--black);
  }

  .upload-card.uploaded {
    border-color: var(--green);
    background: var(--green-bg);
  }

  .upload-card input[type="file"] {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
    width: 100%;
    height: 100%;
  }

  .upload-card-icon {
    font-size: 22px;
    margin-bottom: 10px;
    display: block;
  }

  .upload-card-title {
    font-size: 13px;
    font-weight: 600;
    color: var(--black);
    margin-bottom: 3px;
  }

  .upload-card-hint {
    font-size: 12px;
    color: var(--gray-3);
  }

  .upload-card-filename {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--green);
    margin-top: 6px;
    font-weight: 600;
    word-break: break-all;
  }

  /* ── Button ── */
  .btn-primary {
    width: 100%;
    padding: 15px 20px;
    background: var(--black);
    color: var(--white);
    border: none;
    border-radius: var(--radius);
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.04em;
    cursor: pointer;
    transition: background 0.15s ease;
    text-transform: uppercase;
  }

  .btn-primary:hover:not(:disabled) {
    background: #2a2a2a;
  }

  .btn-primary:disabled {
    background: var(--gray-2);
    color: var(--gray-3);
    cursor: not-allowed;
  }

  /* ── Status messages ── */
  .status-line {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--gray-4);
    margin-top: 10px;
    text-align: center;
    min-height: 18px;
  }

  .status-line::before {
    content: '> ';
    color: var(--accent);
  }

  .error-bar {
    margin-top: 12px;
    padding: 12px 16px;
    background: var(--red-bg);
    border-left: 3px solid var(--red);
    border-radius: var(--radius);
    font-size: 13px;
    color: var(--red);
    font-family: var(--mono);
  }

  /* ── Section separator ── */
  .section-sep {
    border: none;
    border-top: 1.5px solid var(--gray-2);
    margin: 44px 0 36px;
  }

  .section-heading {
    font-size: 11px;
    font-family: var(--mono);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--gray-4);
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--gray-2);
  }

  /* ── Skill gap cards ── */
  .skill-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 44px;
  }

  @media (max-width: 560px) {
    .skill-row { grid-template-columns: 1fr; }
  }

  .skill-card {
    border-radius: var(--radius);
    padding: 18px;
    border: 1.5px solid;
  }

  .skill-card.has {
    border-color: #b8dfc9;
    background: var(--green-bg);
  }

  .skill-card.gap {
    border-color: #f0c4ac;
    background: var(--red-bg);
  }

  .skill-card-header {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 12px;
  }

  .skill-card.has .skill-card-header { color: var(--green); }
  .skill-card.gap .skill-card-header { color: var(--red); }

  .skill-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .pill {
    font-size: 12px;
    padding: 3px 10px;
    border-radius: 2px;
    font-family: var(--mono);
    border: 1px solid;
  }

  .skill-card.has .pill {
    background: #d4efe2;
    border-color: #a8d8bc;
    color: var(--green);
  }

  .skill-card.gap .pill {
    background: #fde0d0;
    border-color: #f5bda0;
    color: var(--red);
  }

  /* ── Roadmap ── */
  .roadmap-count {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--gray-3);
    margin-left: 6px;
  }

  .roadmap-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .roadmap-card {
    border: 1.5px solid var(--gray-2);
    border-radius: var(--radius);
    padding: 18px 20px;
    display: grid;
    grid-template-columns: 56px 1fr;
    gap: 18px;
    align-items: start;
    transition: border-color 0.15s ease;
  }

  .roadmap-card:hover {
    border-color: var(--gray-3);
  }

  .week-col {
    text-align: center;
    padding-top: 3px;
  }

  .week-num {
    font-family: var(--mono);
    font-size: 18px;
    font-weight: 600;
    color: var(--black);
    line-height: 1;
  }

  .week-text {
    font-family: var(--mono);
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--gray-3);
    margin-top: 2px;
  }

  .course-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--black);
    margin-bottom: 6px;
    line-height: 1.3;
  }

  .course-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    flex-wrap: wrap;
  }

  .level-chip {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 2px 8px;
    border-radius: 2px;
    border: 1px solid;
  }

  .level-chip.beginner {
    color: var(--green);
    border-color: #a8d8bc;
    background: var(--green-bg);
  }

  .level-chip.intermediate {
    color: #555;
    border-color: var(--gray-2);
    background: var(--gray-1);
  }

  .level-chip.advanced {
    color: var(--red);
    border-color: #f5bda0;
    background: var(--red-bg);
  }

  .duration-text {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--gray-3);
  }

  .course-reason {
    font-size: 13px;
    color: var(--gray-4);
    line-height: 1.6;
    padding-left: 12px;
    border-left: 2px solid var(--gray-2);
  }

  /* ── Vertical connector between cards ── */
  .roadmap-list li:not(:last-child) .roadmap-card {
    border-bottom-left-radius: var(--radius);
    border-bottom-right-radius: var(--radius);
  }

  /* ── Footer ── */
  .footer {
    margin-top: 72px;
    padding-top: 20px;
    border-top: 1px solid var(--gray-2);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
  }

  .footer-left {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--gray-3);
  }

  .footer-right {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--gray-3);
  }
`;

export default function App() {
  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!resume || !jd) {
      setError("Please upload both a resume and a job description PDF.");
      return;
    }
    setError("");
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("jd", jd);

    try {
      const res = await fetch("https://pathforge-ai-backend.onrender.com/analyze", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setResult(data);
    } catch (e) {
      setError(e.message || "Something went wrong. Is the backend running on port 8000?");
    }

    setLoading(false);
  };

  const levelClass = (level = "") => {
    const l = level.toLowerCase();
    if (l === "intermediate") return "intermediate";
    if (l === "advanced") return "advanced";
    return "beginner";
  };

  return (
    <>
      <style>{styles}</style>
      <div className="page">

        {/* ── Topbar ── */}
        <nav className="topbar">
          <div className="topbar-left">
            <span className="logo">PathForge<span className="logo-dot">.</span>AI</span>
            <span className="tagline">adaptive onboarding engine</span>
          </div>
          <span className="version-badge">v1.0</span>
        </nav>

        {/* ── Intro ── */}
        <div className="intro">
          <h1>Build your personalized<br />learning roadmap</h1>
          <p>
            Upload your resume and target job description. Our engine identifies
            exactly what skills you're missing and maps a week-by-week training plan.
          </p>
        </div>

        {/* ── Upload ── */}
        <span className="label">Step 1 — Upload documents</span>
        <div className="upload-grid">
          <label className={`upload-card ${resume ? "uploaded" : ""}`}>
            <input
              type="file"
              accept=".pdf"
              onChange={e => setResume(e.target.files[0])}
            />
            <span className="upload-card-icon">📄</span>
            <div className="upload-card-title">Resume</div>
            {resume
              ? <div className="upload-card-filename">✓ {resume.name}</div>
              : <div className="upload-card-hint">Click to upload PDF</div>
            }
          </label>

          <label className={`upload-card ${jd ? "uploaded" : ""}`}>
            <input
              type="file"
              accept=".pdf"
              onChange={e => setJd(e.target.files[0])}
            />
            <span className="upload-card-icon">💼</span>
            <div className="upload-card-title">Job Description</div>
            {jd
              ? <div className="upload-card-filename">✓ {jd.name}</div>
              : <div className="upload-card-hint">Click to upload PDF</div>
            }
          </label>
        </div>

        {/* ── Submit ── */}
        <span className="label" style={{ marginTop: "24px" }}>Step 2 — Analyze</span>
        <button
          className="btn-primary"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Generate Learning Roadmap →"}
        </button>

        {loading && (
          <p className="status-line">
            Running skill extraction via local AI model. Please wait...
          </p>
        )}

        {error && <div className="error-bar">Error: {error}</div>}

        {/* ── Results ── */}
        {result && (
          <>
            <hr className="section-sep" />

            {/* Skill Gap */}
            <div className="section-heading">Skill Gap Analysis</div>
            <div className="skill-row">
              <div className="skill-card has">
                <div className="skill-card-header">✓ You already have</div>
                <div className="skill-pills">
                  {(result.candidate_skills || []).map(s => (
                    <span key={s} className="pill">{s}</span>
                  ))}
                </div>
              </div>
              <div className="skill-card gap">
                <div className="skill-card-header">✗ Skills to develop</div>
                <div className="skill-pills">
                  {(result.skill_gap || []).map(s => (
                    <span key={s} className="pill">{s}</span>
                  ))}
                </div>
              </div>
            </div>

            {/* Roadmap */}
            <div className="section-heading">
              Learning Roadmap
              <span className="roadmap-count">
                {result.learning_pathway?.length || 0} courses
              </span>
            </div>
            <ul className="roadmap-list">
              {(result.learning_pathway || []).map((item, i) => (
                <li key={i}>
                  <div className="roadmap-card">
                    <div className="week-col">
                      <div className="week-num">{item.week}</div>
                      <div className="week-text">week</div>
                    </div>
                    <div>
                      <div className="course-title">{item.course_title}</div>
                      <div className="course-meta">
                        <span className={`level-chip ${levelClass(item.level)}`}>
                          {item.level || "beginner"}
                        </span>
                        <span className="duration-text">{item.duration}</span>
                      </div>
                      <div className="course-reason">{item.reason}</div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </>
        )}

        {/* ── Footer ── */}
        <footer className="footer">
          <span className="footer-left">PathForge AI · ARTPARK CodeForge Hackathon</span>
          <span className="footer-right">FastAPI + React + Ollama (Mistral 7B)</span>
        </footer>

      </div>
    </>
  );
}
