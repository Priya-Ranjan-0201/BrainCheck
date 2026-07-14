"""
BrainCheck — Automated Tests
Tests: app startup, routes, score calculation, health check.
"""

import pytest
from app import app, QUESTIONS


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# -----------------------------------------------------------------------
# 1. Application starts successfully
# -----------------------------------------------------------------------
def test_app_exists():
    """The Flask app instance should exist."""
    assert app is not None


def test_app_is_testing(client):
    """App should be in testing mode."""
    assert app.config["TESTING"] is True


# -----------------------------------------------------------------------
# 2. Home page loads
# -----------------------------------------------------------------------
def test_home_page_status(client):
    """GET / should return 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_content(client):
    """Home page should contain the app name."""
    response = client.get("/")
    assert b"BrainCheck" in response.data


# -----------------------------------------------------------------------
# 3. Quiz page loads
# -----------------------------------------------------------------------
def test_quiz_page_status(client):
    """GET /quiz should return 200."""
    response = client.get("/quiz")
    assert response.status_code == 200


def test_quiz_page_has_questions(client):
    """Quiz page should contain all 5 questions."""
    response = client.get("/quiz")
    for q in QUESTIONS:
        assert q["question"].encode() in response.data


def test_quiz_page_has_submit(client):
    """Quiz page should have a submit button."""
    response = client.get("/quiz")
    assert b"Submit" in response.data


# -----------------------------------------------------------------------
# 4. Score calculation works
# -----------------------------------------------------------------------
def test_result_all_correct(client):
    """Submitting all correct answers should give 100%."""
    data = {f"question_{q['id']}": str(q["answer"]) for q in QUESTIONS}
    response = client.post("/result", data=data)
    assert response.status_code == 200
    assert b"100%" in response.data
    assert b"5" in response.data


def test_result_all_wrong(client):
    """Submitting all wrong answers should give 0%."""
    data = {}
    for q in QUESTIONS:
        wrong = (q["answer"] + 1) % len(q["options"])
        data[f"question_{q['id']}"] = str(wrong)
    response = client.post("/result", data=data)
    assert response.status_code == 200
    assert b"0%" in response.data


def test_result_partial_score(client):
    """Submitting some correct answers should give partial score."""
    data = {}
    for i, q in enumerate(QUESTIONS):
        if i < 3:  # First 3 correct
            data[f"question_{q['id']}"] = str(q["answer"])
        else:  # Last 2 wrong
            data[f"question_{q['id']}"] = str((q["answer"] + 1) % len(q["options"]))
    response = client.post("/result", data=data)
    assert response.status_code == 200
    assert b"60%" in response.data


def test_result_no_answers(client):
    """Submitting with no answers should give 0%."""
    response = client.post("/result", data={})
    assert response.status_code == 200
    assert b"0%" in response.data


# -----------------------------------------------------------------------
# 5. Health check endpoint
# -----------------------------------------------------------------------
def test_health_check(client):
    """GET /health should return 200 with healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


# -----------------------------------------------------------------------
# 6. Questions data integrity
# -----------------------------------------------------------------------
def test_questions_count():
    """There should be exactly 5 questions."""
    assert len(QUESTIONS) == 5


def test_questions_have_required_fields():
    """Each question should have id, question, options, and answer."""
    for q in QUESTIONS:
        assert "id" in q
        assert "question" in q
        assert "options" in q
        assert "answer" in q
        assert len(q["options"]) == 4
        assert 0 <= q["answer"] < 4
