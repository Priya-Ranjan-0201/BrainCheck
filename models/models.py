"""
Database Models

Defines the four core tables:
    • User          – registered users and admins
    • QuizCategory  – quiz topic groupings
    • Question      – multiple-choice questions
    • QuizAttempt   – completed quiz records with scores
"""

from datetime import datetime, timezone
from flask_login import UserMixin
from app import db


# ──────────────────────────────────────────────
# User
# ──────────────────────────────────────────────
class User(UserMixin, db.Model):
    """Application user (student or admin)."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # 'user' | 'admin'
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    attempts = db.relationship(
        "QuizAttempt", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def is_admin(self):
        """Return True if the user has admin privileges."""
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.email}>"


# ──────────────────────────────────────────────
# Quiz Category
# ──────────────────────────────────────────────
class QuizCategory(db.Model):
    """Grouping for quiz questions (e.g. Python, Docker)."""

    __tablename__ = "quiz_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relationships
    questions = db.relationship(
        "Question", backref="category", lazy="dynamic", cascade="all, delete-orphan"
    )
    attempts = db.relationship(
        "QuizAttempt", backref="category", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<QuizCategory {self.name}>"


# ──────────────────────────────────────────────
# Question
# ──────────────────────────────────────────────
class Question(db.Model):
    """A single multiple-choice question."""

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey("quiz_categories.id"), nullable=False, index=True
    )
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # 'A' | 'B' | 'C' | 'D'

    def __repr__(self):
        return f"<Question {self.id}: {self.question[:40]}>"


# ──────────────────────────────────────────────
# Quiz Attempt
# ──────────────────────────────────────────────
class QuizAttempt(db.Model):
    """Records a completed quiz with the user's score."""

    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("quiz_categories.id"), nullable=False, index=True
    )
    score = db.Column(db.Integer, nullable=False, default=0)
    total_questions = db.Column(db.Integer, nullable=False, default=0)
    percentage = db.Column(db.Float, nullable=False, default=0.0)
    completed_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<QuizAttempt user={self.user_id} score={self.score}/{self.total_questions}>"
