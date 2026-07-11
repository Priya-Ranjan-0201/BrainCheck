"""
Application Configuration

Centralises all Flask and extension settings.
Values are read from environment variables with sensible defaults,
making the app 12-factor compliant and Docker-friendly.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration used by the application factory."""

    # ── Secret key (sessions & CSRF) ─────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "quiz-app-super-secret-key-change-me")

    # ── SQLAlchemy ───────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Flask-WTF ────────────────────────────
    WTF_CSRF_ENABLED = True

    # ── Quiz settings ────────────────────────
    QUIZ_TIME_LIMIT = int(os.environ.get("QUIZ_TIME_LIMIT", 300))  # seconds (5 min)

    # ── Session Cookie Security ──────────────
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False").lower() == "true"
    SESSION_COOKIE_HTTPONLY = os.environ.get("SESSION_COOKIE_HTTPONLY", "True").lower() == "true"
    SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax")

    # ── Admin defaults ───────────────────────
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@quizapp.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@123")


class TestingConfig(Config):
    """Overrides for the test suite."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "testing-secret-key"
