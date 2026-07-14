"""
BrainCheck - A minimal Flask quiz app for DevOps demonstration.
"""

import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# ---------------------------------------------------------------------------
# Quiz Data — 5 hardcoded multiple-choice questions
# ---------------------------------------------------------------------------
QUESTIONS = [
    {
        "id": 1,
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Central Program Utility",
            "Computer Personal Unit",
            "Central Processor Unifier",
        ],
        "answer": 0,
    },
    {
        "id": 2,
        "question": "Which command is used to list files in Linux?",
        "options": ["dir", "ls", "list", "show"],
        "answer": 1,
    },
    {
        "id": 3,
        "question": "What does HTML stand for?",
        "options": [
            "Hyper Trainer Marking Language",
            "Hyper Text Marketing Language",
            "Hyper Text Markup Language",
            "High Tech Modern Language",
        ],
        "answer": 2,
    },
    {
        "id": 4,
        "question": "Which protocol is used to send emails?",
        "options": ["FTP", "HTTP", "SMTP", "SSH"],
        "answer": 2,
    },
    {
        "id": 5,
        "question": "What is Docker used for?",
        "options": [
            "Writing code",
            "Containerization",
            "Email hosting",
            "Video editing",
        ],
        "answer": 1,
    },
]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    """Landing page."""
    return render_template("home.html")


@app.route("/quiz")
def quiz():
    """Display the quiz with all 5 questions."""
    return render_template("quiz.html", questions=QUESTIONS)


@app.route("/result", methods=["POST"])
def result():
    """Calculate and display the score."""
    score = 0
    total = len(QUESTIONS)

    for q in QUESTIONS:
        selected = request.form.get(f"question_{q['id']}")
        if selected is not None and int(selected) == q["answer"]:
            score += 1

    percentage = int((score / total) * 100)
    return render_template(
        "result.html", score=score, total=total, percentage=percentage
    )


@app.route("/health")
def health():
    """Health check endpoint for Docker / CI."""
    return {"status": "healthy"}, 200


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
