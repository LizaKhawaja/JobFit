# JobFit
### AI-powered Resume Screener

JobFit analyzes your resume against a job description using AI and gives you a detailed match report including a match score, matched and missing skills, strengths, and improvement suggestions. Every analysis is saved to a PostgreSQL database and can be retrieved later.

---

## Features

- Match score (0-100) between resume and job description
- Matched and missing skills breakdown
- Candidate strengths analysis
- Actionable improvement suggestions
- Clean UI with instant results
- **Output validation:** the AI response is checked with Pydantic (score must be 0-100, all fields must be present) before it reaches the user
- **Prompt injection mitigation:** instructions and user data are sent separately, and the resume and job description are wrapped in tags and treated as data only
- **Input limits:** resume and job description are capped at 15,000 characters each to protect API quota
- **Safe error handling:** users see generic error messages, while detailed errors are logged server-side
- **History:** every analysis is saved to PostgreSQL and available through a `/history` endpoint
- **Automated tests:** pytest tests cover validation, error handling and the AI response flow, with the AI API and database mocked

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| AI Model | `openai/gpt-oss-120b` via Groq API |
| Database | PostgreSQL, SQLAlchemy |
| Frontend | HTML, CSS, JavaScript |
| Validation | Pydantic |
| Testing | pytest |

---

## How It Works

1. The user submits a resume and job description to `POST /analyze`
2. FastAPI and Pydantic validate the input (types, empty values, length limit)
3. A prompt is built: instructions go in the `system` message, and the data goes in the `user` message inside `<resume>` and `<job_description>` tags
4. The request is sent to the model on Groq with `temperature=0` and JSON mode enabled
5. The response is parsed and validated against a Pydantic model
6. The result is saved to PostgreSQL and returned to the user

---

## Project Structure

```text
jobfit/
├── main.py          # FastAPI backend and API endpoints
├── database.py      # Database connection and session
├── models.py        # SQLAlchemy table (analyses)
├── test_main.py     # pytest tests
├── index.html       # Frontend UI
├── .env             # API key and database settings (not committed)
├── requirements.txt # Python dependencies
└── .gitignore
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/LizaKhawaja/jobfit.git
cd jobfit
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL
Install PostgreSQL, then create a database:
```sql
CREATE DATABASE jobfit;
```
The `analyses` table is created automatically when the app starts.

### 5. Set up environment variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/jobfit
```

Get your free API key at: https://console.groq.com

### 6. Run the backend
```bash
uvicorn main:app --reload
```

### 7. Open the frontend
Open `index.html` directly in your browser.

---

## Running Tests

```bash
pytest -v
```

The tests mock the Groq API and the database, so they do not use API tokens and do not write to your database. PostgreSQL still needs to be running, because the app creates its tables when it is imported.

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

**Status codes:**

| Code | Meaning |
|------|---------|
| 200 | Analysis successful |
| 400 | Resume or job description is empty |
| 422 | Invalid request (missing field, wrong type, or text over 15,000 characters) |
| 502 | The AI returned an invalid response |
| 500 | Unexpected server error |

### Endpoint: `GET /history`

Returns the most recent analyses (default 10, maximum 50).

**Query parameter:** `limit` (optional)

**Response:**
```json
[
  {
    "id": 1,
    "match_score": 40,
    "summary": "Solid foundation in Python and FastAPI, but lacks Docker and AWS...",
    "created_at": "2026-10-30T10:45:12+00:00"
  }
]
```

### Endpoint: `GET /`

Health check. Returns a message confirming the API is running.

---

## Limitations

- **The match score is an AI estimate, not a formula.** The model predicts the score using a scoring guide in the prompt. It is generally sensible but can be inconsistent, and it may sometimes mark a skill as missing when it is only implied in the resume (for example, REST API experience from building FastAPI projects).
- **Prompt injection mitigation is not a guarantee.** Separating instructions from data and tagging the input reduces the risk, but it cannot fully eliminate it.
- **`/history` has no authentication.** It is meant for local use. It should be protected before any public deployment, since saved resumes contain personal data.
- **CORS is open (`*`)** for development convenience and should be restricted in production.
- **Free-tier limits.** The Groq free tier has rate and token limits, so heavy use may return errors.

---

## Future Improvements

- Calculate the score with a custom weighted formula (the model would only extract skills and experience)
- Authentication and per-user history
- Response caching for repeated resume and job description pairs
- Docker setup and live deployment

---

## Screenshots

![Home Page](Screenshots/home.png)
![High Match Result](Screenshots/highScore.png)
![Low Match Result](Screenshots/mediumLow_score.png)

## Author

Built by [Liza Khawaja](https://github.com/LizaKhawaja)