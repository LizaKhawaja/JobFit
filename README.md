# JobFit 
### AI-powered Resume Screener

JobFit analyzes your resume against a job description using AI and gives you a detailed match report including match score, missing skills, strengths, and improvement suggestions.

---

## Features

- Match score (0-100%) between resume and job description
- Matched and missing skills breakdown
- Candidate strengths analysis
- Actionable improvement suggestions
- Clean UI with instant results

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| AI Model | Llama 3.3 70B via Groq API |
| Frontend | HTML, CSS, JavaScript |
| Validation | Pydantic |

---

## Project Structure
jobfit/
├── main.py          # FastAPI backend + API endpoints
├── index.html       # Frontend UI
├── .env             # API keys (not committed)
├── requirements.txt # Python dependencies
└── .gitignore

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/LizaKhawaja/jobfit.git
cd jobfit
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
GROQ_API_KEY=your_groq_api_key_here

Get your free API key at: https://console.groq.com

### 5. Run the backend
```bash
uvicorn main:app --reload
```

### 6. Open the frontend
Open `index.html` directly in your browser.

---

## API Documentation

FastAPI provides automatic interactive docs at:
http://127.0.0.1:8000/docs

### Endpoint: `POST /analyze`

**Request Body:**
```json
{
  "resume": "Your resume text here",
  "job_description": "Job description text here"
}
```

**Response:**
```json
{
  "match_score": 85,
  "matched_skills": ["Python", "FastAPI", "Git"],
  "missing_skills": ["Docker", "Kubernetes"],
  "strengths": ["Strong Python background", "..."],
  "suggestions": ["Learn Docker", "..."],
  "summary": "Strong candidate with relevant experience..."
}
```

---

## Screenshots

![Home Page](screenshots/home.png)
![High Match Result](screenshots/highScore.png)
![Low Match Result](screenshots/mediumLow_score.png)

## Author

Built by [Liza Khawaja](https://github.com/LizaKhawaja)