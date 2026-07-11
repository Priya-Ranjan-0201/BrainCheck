"""
Admin Routes

Provides the admin dashboard and full CRUD operations for:
    • Quiz Categories  – create / delete
    • Questions        – add / edit / delete
    • Users            – view registered users
    • Quiz Attempts    – view all scores
"""

from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models.models import User, QuizCategory, Question, QuizAttempt

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ──────────────────────────────────────────────
# Admin-only decorator
# ──────────────────────────────────────────────
def admin_required(f):
    """Restrict access to users with the 'admin' role."""

    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for("main.dashboard"))
        return f(*args, **kwargs)

    return decorated_function


# ──────────────────────────────────────────────
# Admin Dashboard
# ──────────────────────────────────────────────
@admin_bp.route("/")
@admin_required
def dashboard():
    """Admin overview with aggregate statistics."""

    total_users = User.query.filter_by(role="user").count()
    total_admins = User.query.filter_by(role="admin").count()
    total_categories = QuizCategory.query.count()
    total_questions = Question.query.count()
    total_attempts = QuizAttempt.query.count()

    # Average score across all attempts
    all_attempts = QuizAttempt.query.all()
    avg_score = (
        round(sum(a.percentage for a in all_attempts) / len(all_attempts), 1)
        if all_attempts
        else 0.0
    )

    # Recent attempts (last 10)
    recent_attempts = (
        QuizAttempt.query.order_by(QuizAttempt.completed_at.desc()).limit(10).all()
    )

    # Category breakdown
    categories = QuizCategory.query.all()
    category_stats = []
    for cat in categories:
        q_count = Question.query.filter_by(category_id=cat.id).count()
        a_count = QuizAttempt.query.filter_by(category_id=cat.id).count()
        category_stats.append(
            {"name": cat.name, "questions": q_count, "attempts": a_count}
        )

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_admins=total_admins,
        total_categories=total_categories,
        total_questions=total_questions,
        total_attempts=total_attempts,
        avg_score=avg_score,
        recent_attempts=recent_attempts,
        category_stats=category_stats,
    )


# ══════════════════════════════════════════════
#  CATEGORIES
# ══════════════════════════════════════════════


@admin_bp.route("/categories", methods=["GET", "POST"])
@admin_required
def categories():
    """List categories and handle creation of new ones."""

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if not name:
            flash("Category name is required.", "danger")
        elif QuizCategory.query.filter_by(name=name).first():
            flash("A category with this name already exists.", "warning")
        else:
            db.session.add(QuizCategory(name=name))
            db.session.commit()
            flash(f"Category '{name}' created successfully.", "success")

        return redirect(url_for("admin.categories"))

    cats = QuizCategory.query.all()
    category_data = []
    for cat in cats:
        q_count = Question.query.filter_by(category_id=cat.id).count()
        category_data.append({"id": cat.id, "name": cat.name, "question_count": q_count})

    return render_template("admin/categories.html", categories=category_data)


@admin_bp.route("/categories/delete/<int:category_id>", methods=["POST"])
@admin_required
def delete_category(category_id):
    """Delete a category and all its questions + attempts (cascade)."""

    category = QuizCategory.query.get_or_404(category_id)
    name = category.name
    db.session.delete(category)
    db.session.commit()
    flash(f"Category '{name}' and all related data deleted.", "success")
    return redirect(url_for("admin.categories"))


# ══════════════════════════════════════════════
#  QUESTIONS
# ══════════════════════════════════════════════


@admin_bp.route("/questions")
@admin_required
def questions():
    """List all questions, optionally filtered by category."""

    category_id = request.args.get("category_id", type=int)

    if category_id:
        all_questions = (
            Question.query.filter_by(category_id=category_id)
            .order_by(Question.id.desc())
            .all()
        )
    else:
        all_questions = Question.query.order_by(Question.id.desc()).all()

    categories_list = QuizCategory.query.all()

    return render_template(
        "admin/questions.html",
        questions=all_questions,
        categories=categories_list,
        selected_category=category_id,
    )


@admin_bp.route("/questions/add", methods=["GET", "POST"])
@admin_required
def add_question():
    """Add a new question to the database."""

    if request.method == "POST":
        category_id = request.form.get("category_id", type=int)
        question_text = request.form.get("question", "").strip()
        option_a = request.form.get("option_a", "").strip()
        option_b = request.form.get("option_b", "").strip()
        option_c = request.form.get("option_c", "").strip()
        option_d = request.form.get("option_d", "").strip()
        correct_option = request.form.get("correct_option", "").strip().upper()

        # Validation
        errors = []
        if not category_id:
            errors.append("Please select a category.")
        if not question_text:
            errors.append("Question text is required.")
        if not all([option_a, option_b, option_c, option_d]):
            errors.append("All four options are required.")
        if correct_option not in ("A", "B", "C", "D"):
            errors.append("Please select a valid correct option (A, B, C, or D).")

        if errors:
            for err in errors:
                flash(err, "danger")
            categories_list = QuizCategory.query.all()
            return render_template(
                "admin/add_question.html",
                categories=categories_list,
                form_data=request.form,
            )

        question = Question(
            category_id=category_id,
            question=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option,
        )
        db.session.add(question)
        db.session.commit()

        flash("Question added successfully.", "success")
        return redirect(url_for("admin.questions"))

    categories_list = QuizCategory.query.all()
    return render_template("admin/add_question.html", categories=categories_list)


@admin_bp.route("/questions/edit/<int:question_id>", methods=["GET", "POST"])
@admin_required
def edit_question(question_id):
    """Edit an existing question."""

    question = Question.query.get_or_404(question_id)

    if request.method == "POST":
        category_id = request.form.get("category_id", type=int)
        question_text = request.form.get("question", "").strip()
        option_a = request.form.get("option_a", "").strip()
        option_b = request.form.get("option_b", "").strip()
        option_c = request.form.get("option_c", "").strip()
        option_d = request.form.get("option_d", "").strip()
        correct_option = request.form.get("correct_option", "").strip().upper()

        # Validation
        errors = []
        if not category_id:
            errors.append("Please select a category.")
        if not question_text:
            errors.append("Question text is required.")
        if not all([option_a, option_b, option_c, option_d]):
            errors.append("All four options are required.")
        if correct_option not in ("A", "B", "C", "D"):
            errors.append("Please select a valid correct option (A, B, C, or D).")

        if errors:
            for err in errors:
                flash(err, "danger")
            categories_list = QuizCategory.query.all()
            return render_template(
                "admin/edit_question.html",
                question=question,
                categories=categories_list,
            )

        question.category_id = category_id
        question.question = question_text
        question.option_a = option_a
        question.option_b = option_b
        question.option_c = option_c
        question.option_d = option_d
        question.correct_option = correct_option
        db.session.commit()

        flash("Question updated successfully.", "success")
        return redirect(url_for("admin.questions"))

    categories_list = QuizCategory.query.all()
    return render_template(
        "admin/edit_question.html",
        question=question,
        categories=categories_list,
    )


@admin_bp.route("/questions/delete/<int:question_id>", methods=["POST"])
@admin_required
def delete_question(question_id):
    """Delete a single question."""

    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully.", "success")
    return redirect(url_for("admin.questions"))


# ══════════════════════════════════════════════
#  USERS
# ══════════════════════════════════════════════


@admin_bp.route("/users")
@admin_required
def users():
    """List all registered users."""

    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users)


# ══════════════════════════════════════════════
#  QUIZ ATTEMPTS / SCORES
# ══════════════════════════════════════════════


@admin_bp.route("/attempts")
@admin_required
def attempts():
    """List all quiz attempts across all users."""

    all_attempts = (
        QuizAttempt.query.order_by(QuizAttempt.completed_at.desc()).all()
    )
    return render_template("admin/attempts.html", attempts=all_attempts)
