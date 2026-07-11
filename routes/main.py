"""
Main Routes

Serves the user-facing dashboard with statistics,
recent quiz attempts, and available quiz categories.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.models import QuizCategory, QuizAttempt, Question

main_bp = Blueprint("main", __name__, url_prefix="/dashboard")


# ──────────────────────────────────────────────
# User Dashboard
# ──────────────────────────────────────────────
@main_bp.route("/")
@login_required
def dashboard():
    """
    Display the authenticated user's dashboard.

    Shows:
        • Total quizzes taken
        • Average score percentage
        • Best score percentage
        • Available quiz categories (with question counts)
        • Five most recent attempts
    """

    # ── Aggregate stats ──────────────────────
    user_attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()
    total_quizzes = len(user_attempts)

    if total_quizzes > 0:
        avg_score = round(
            sum(a.percentage for a in user_attempts) / total_quizzes, 1
        )
        best_score = round(max(a.percentage for a in user_attempts), 1)
    else:
        avg_score = 0.0
        best_score = 0.0

    # ── Available categories ─────────────────
    categories = QuizCategory.query.all()
    category_data = []
    for cat in categories:
        question_count = Question.query.filter_by(category_id=cat.id).count()
        category_data.append(
            {
                "id": cat.id,
                "name": cat.name,
                "question_count": question_count,
            }
        )

    # ── Recent attempts (last 5) ─────────────
    recent_attempts = (
        QuizAttempt.query.filter_by(user_id=current_user.id)
        .order_by(QuizAttempt.completed_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "main/dashboard.html",
        total_quizzes=total_quizzes,
        avg_score=avg_score,
        best_score=best_score,
        categories=category_data,
        recent_attempts=recent_attempts,
    )
