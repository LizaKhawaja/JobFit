import json
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

import main
from database import get_db

api = TestClient(main.app)


def fake_db():
    yield MagicMock()


main.app.dependency_overrides[get_db] = fake_db


VALID_RESULT = {
    "match_score": 72,
    "matched_skills": ["Python"],
    "missing_skills": ["Docker"],
    "strengths": ["Strong Python", "Good projects", "Clear writing"],
    "suggestions": ["Learn Docker", "Learn AWS", "Add metrics"],
    "summary": "Good fit overall. Needs Docker experience.",
}

VALID_BODY = {"resume": "Python developer", "job_description": "Backend developer"}


def fake_groq_response(content):
    response = MagicMock()
    response.choices[0].message.content = content
    return response


def test_root():
    response = api.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "JobFit API is running!"}


def test_empty_resume_returns_400():
    response = api.post("/analyze", json={"resume": "   ", "job_description": "Backend developer"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Resume cannot be empty"


def test_empty_job_description_returns_400():
    response = api.post("/analyze", json={"resume": "Python developer", "job_description": "   "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Job description cannot be empty"


def test_missing_field_returns_422():
    response = api.post("/analyze", json={"resume": "Python developer"})
    assert response.status_code == 422


def test_too_long_input_returns_422_and_skips_groq():
    with patch("main.client") as mock_client:
        response = api.post(
            "/analyze",
            json={"resume": "a" * 20000, "job_description": "Backend developer"},
        )
    assert response.status_code == 422
    mock_client.chat.completions.create.assert_not_called()


def test_successful_analysis():
    with patch("main.client") as mock_client:
        mock_client.chat.completions.create.return_value = fake_groq_response(
            json.dumps(VALID_RESULT)
        )
        response = api.post("/analyze", json=VALID_BODY)
    assert response.status_code == 200
    assert response.json()["match_score"] == 72
    assert response.json()["missing_skills"] == ["Docker"]


def test_score_out_of_range_returns_502():
    bad_result = {**VALID_RESULT, "match_score": 150}
    with patch("main.client") as mock_client:
        mock_client.chat.completions.create.return_value = fake_groq_response(
            json.dumps(bad_result)
        )
        response = api.post("/analyze", json=VALID_BODY)
    assert response.status_code == 502


def test_invalid_json_from_model_returns_502():
    with patch("main.client") as mock_client:
        mock_client.chat.completions.create.return_value = fake_groq_response("this is not json")
        response = api.post("/analyze", json=VALID_BODY)
    assert response.status_code == 502


def test_groq_failure_returns_500_without_leaking_details():
    with patch("main.client") as mock_client:
        mock_client.chat.completions.create.side_effect = Exception("secret internal error")
        response = api.post("/analyze", json=VALID_BODY)
    assert response.status_code == 500
    assert "secret" not in response.text