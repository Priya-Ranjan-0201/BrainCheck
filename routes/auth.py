"""
Authentication Routes

Handles user registration, login, and logout.
Passwords are hashed with Werkzeug's PBKDF2 implementation.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ──────────────────────────────────────────────
# Register
# ──────────────────────────────────────────────
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Create a new user account."""

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # ── Validation ───────────────────────
        errors = []

        if not fullname:
            errors.append("Full name is required.")
        if not email:
            errors.append("Email is required.")
        if not password:
            errors.append("Password is required.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if User.query.filter_by(email=email).first():
            errors.append("An account with this email already exists.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "auth/register.html",
                fullname=fullname,
                email=email,
            )

        # ── Create user ──────────────────────
        user = User(
            fullname=fullname,
            email=email,
            password_hash=generate_password_hash(password),
            role="user",
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ──────────────────────────────────────────────
# Login
# ──────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate an existing user."""

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            flash(f"Welcome back, {user.fullname}!", "success")

            # Redirect to the page the user originally requested
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)

            # Admin → admin dashboard; User → user dashboard
            if user.is_admin:
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "danger")
        return render_template("auth/login.html", email=email)

    return render_template("auth/login.html")


# ──────────────────────────────────────────────
# Logout
# ──────────────────────────────────────────────
@auth_bp.route("/logout")
@login_required
def logout():
    """Log the current user out and redirect to login."""

    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
