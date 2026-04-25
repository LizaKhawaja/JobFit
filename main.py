from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(title="JobFit", description="AI Resume Screener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    resume: str
    job_description: str

@app.get("/")
def root():
    return {"message": "JobFit API is running!"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    if not request.resume.strip():
        raise HTTPException(status_code=400, detail="Resume cannot be empty")
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    prompt = f"""
You are an expert recruiter and resume analyst.
Analyze the resume against the job description and return ONLY a valid JSON object.
No explanation, no markdown, no extra text — just raw JSON.

{{
  "match_score": <number 0-100>,
  "matched_skills": [<list of matching skills>],
  "missing_skills": [<list of missing skills>],
  "strengths": [<list of 3 candidate strengths>],
  "suggestions": [<list of 3 specific improvements>],
  "summary": "<2 sentence overall assessment>"
}}

Resume:
{request.resume}

Job Description:
{request.job_description}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        text = response.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text)
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI response could not be parsed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))