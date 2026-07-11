"""
Quiz Routes

Handles the full quiz-taking workflow:
    1. Browse available categories
    2. Start a quiz (questions are randomised and stored in the session)
    3. Navigate one question at a time (next / previous)
    4. Submit answers (manual or auto-submit on timer expiry)
    5. View result with correct answers
    6. Browse previous attempts
"""

import random
from datetime import datetime, timezone

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    current_app,
)
from flask_login import login_required, current_user
from app import db
from models.models import QuizCategory, Question, QuizAttempt

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")


# ──────────────────────────────────────────────
# Browse categories
# ──────────────────────────────────────────────
@quiz_bp.route("/categories")
@login_required
def categories():
    """List all quiz categories with question counts."""

    cats = QuizCategory.query.all()
    category_data = []
    for cat in cats:
        count = Question.query.filter_by(category_id=cat.id).count()
        category_data.append({"id": cat.id, "name": cat.name, "question_count": count})

    return render_template("quiz/categories.html", categories=category_data)


# ──────────────────────────────────────────────
# Start a quiz
# ──────────────────────────────────────────────
@quiz_bp.route("/start/<int:category_id>")
@login_required
def start_quiz(category_id):
    """
    Initialise a new quiz session.

    • Fetches all questions for the category
    • Randomises the order
    • Stores question IDs & answers dict in the Flask session
    • Redirects to the first question
    """

    category = QuizCategory.query.get_or_404(category_id)
    questions = Question.query.filter_by(category_id=category_id).all()

    if not questions:
        flash("No questions available in this category yet.", "warning")
        return redirect(url_for("quiz.categories"))

    # Shuffle and store IDs in the session
    random.shuffle(questions)
    question_ids = [q.id for q in questions]

    session["quiz_category_id"] = category_id
    session["quiz_category_name"] = category.name
    session["quiz_question_ids"] = question_ids
    session["quiz_answers"] = {}  # {question_id: selected_option}
    session["quiz_current"] = 0   # index into question_ids
    session["quiz_time_limit"] = current_app.config["QUIZ_TIME_LIMIT"]
    session["quiz_start_time"] = datetime.now(timezone.utc).isoformat()

    return redirect(url_for("quiz.take_quiz"))


# ──────────────────────────────────────────────
# Take quiz (one question at a time)
# ──────────────────────────────────────────────
@quiz_bp.route("/take", methods=["GET", "POST"])
@login_required
def take_quiz():
    """
    Display the current question and handle navigation.

    GET  → render the current question
    POST → save the selected answer, then navigate (next / prev / submit)
    """

    question_ids = session.get("quiz_question_ids")
    if not question_ids:
        flash("No active quiz session. Please start a quiz first.", "warning")
        return redirect(url_for("quiz.categories"))

    current_index = session.get("quiz_current", 0)
    answers = session.get("quiz_answers", {})
    total = len(question_ids)

    # ── Handle answer submission / navigation ─
    if request.method == "POST":
        # Save the selected answer (if any)
        selected = request.form.get("selected_option")
        current_qid = str(question_ids[current_index])
        if selected:
            answers[current_qid] = selected
            session["quiz_answers"] = answers

        action = request.form.get("action", "next")

        if action == "previous" and current_index > 0:
            session["quiz_current"] = current_index - 1
            return redirect(url_for("quiz.take_quiz"))

        if action == "next" and current_index < total - 1:
            session["quiz_current"] = current_index + 1
            return redirect(url_for("quiz.take_quiz"))

        if action == "submit":
            return redirect(url_for("quiz.submit_quiz"))

    # ── Load the current question ────────────
    question = Question.query.get(question_ids[current_index])
    current_qid_str = str(question_ids[current_index])
    selected_answer = answers.get(current_qid_str, "")

    return render_template(
        "quiz/quiz.html",
        question=question,
        current=current_index + 1,
        total=total,
        selected_answer=selected_answer,
        is_first=(current_index == 0),
        is_last=(current_index == total - 1),
        category_name=session.get("quiz_category_name", "Quiz"),
        time_limit=session.get("quiz_time_limit", 300),
        start_time=session.get("quiz_start_time", ""),
    )


# ──────────────────────────────────────────────
# Submit quiz
# ──────────────────────────────────────────────
@quiz_bp.route("/submit", methods=["GET", "POST"])
@login_required
def submit_quiz():
    """
    Score the quiz and persist the attempt.

    • Compares session answers with correct options
    • Calculates score & percentage
    • Saves a QuizAttempt record
    • Clears the session
    • Redirects to the result page
    """

    question_ids = session.get("quiz_question_ids")
    if not question_ids:
        flash("No active quiz session.", "warning")
        return redirect(url_for("quiz.categories"))

    # If POST with auto-submit data, save the last answer first
    if request.method == "POST":
        selected = request.form.get("selected_option")
        current_index = session.get("quiz_current", 0)
        if selected and current_index < len(question_ids):
            current_qid = str(question_ids[current_index])
            answers = session.get("quiz_answers", {})
            answers[current_qid] = selected
            session["quiz_answers"] = answers

    answers = session.get("quiz_answers", {})
    category_id = session.get("quiz_category_id")

    # ── Score calculation ────────────────────
    score = 0
    total = len(question_ids)
    result_details = []

    for qid in question_ids:
        question = Question.query.get(qid)
        if not question:
            continue

        user_answer = answers.get(str(qid), "")
        is_correct = user_answer.upper() == question.correct_option.upper() if user_answer else False
        if is_correct:
            score += 1

        result_details.append(
            {
                "question": question.question,
                "option_a": question.option_a,
                "option_b": question.option_b,
                "option_c": question.option_c,
                "option_d": question.option_d,
                "correct_option": question.correct_option,
                "user_answer": user_answer,
                "is_correct": is_correct,
            }
        )

    percentage = round((score / total) * 100, 1) if total > 0 else 0.0

    # ── Persist the attempt ──────────────────
    attempt = QuizAttempt(
        user_id=current_user.id,
        category_id=category_id,
        score=score,
        total_questions=total,
        percentage=percentage,
    )
    db.session.add(attempt)
    db.session.commit()

    # ── Store results for the result page ────
    session["quiz_result"] = {
        "score": score,
        "total": total,
        "percentage": percentage,
        "category_name": session.get("quiz_category_name", "Quiz"),
        "details": result_details,
        "attempt_id": attempt.id,
    }

    # ── Clear quiz session data ──────────────
    for key in [
        "quiz_category_id",
        "quiz_category_name",
        "quiz_question_ids",
        "quiz_answers",
        "quiz_current",
        "quiz_time_limit",
        "quiz_start_time",
    ]:
        session.pop(key, None)

    return redirect(url_for("quiz.result"))


# ──────────────────────────────────────────────
# Result page
# ──────────────────────────────────────────────
@quiz_bp.route("/result")
@login_required
def result():
    """Display the score and correct answers after quiz completion."""

    quiz_result = session.pop("quiz_result", None)
    if not quiz_result:
        flash("No quiz result found.", "warning")
        return redirect(url_for("quiz.categories"))

    return render_template("quiz/result.html", result=quiz_result)


# ──────────────────────────────────────────────
# Previous attempts
# ──────────────────────────────────────────────
@quiz_bp.route("/attempts")
@login_required
def attempts():
    """Show all past quiz attempts for the current user."""

    user_attempts = (
        QuizAttempt.query.filter_by(user_id=current_user.id)
        .order_by(QuizAttempt.completed_at.desc())
        .all()
    )

    return render_template("quiz/attempts.html", attempts=user_attempts)
