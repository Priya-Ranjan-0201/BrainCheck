"""
BrainCheck App Configuration
All settings are pulled from environment variables so the app works in any environment.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "braincheck-secret-key-change-me")

    # ── SQLAlchemy ───────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Flask-WTF ────────────────────────────
    WTF_CSRF_ENABLED = True

    QUIZ_TIME_LIMIT = int(os.environ.get("QUIZ_TIME_LIMIT", 300))  # 5 minutes

    # ── Session Cookie Security ──────────────
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False").lower() == "true"
    SESSION_COOKIE_HTTPONLY = os.environ.get("SESSION_COOKIE_HTTPONLY", "True").lower() == "true"
    SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax")

    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@braincheck.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@123")


class TestingConfig(Config):
    """Config overrides for running tests."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "testing-secret-key"
