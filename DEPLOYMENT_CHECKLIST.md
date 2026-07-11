# ============================================================
# Deployment Verification Checklist
# Dockerized Quiz Application
# ============================================================
#
# Run through every item below BEFORE declaring the
# application production-ready. Each section includes the
# exact commands or actions to perform and what "pass"
# looks like.
#
# Legend:
#   [ ] = Not yet verified
#   [x] = Verified and passing
# ============================================================


# ════════════════════════════════════════════════════════════
# 1. DOCKER IMAGE BUILD
# ════════════════════════════════════════════════════════════
#
# Verifies that the Dockerfile produces a valid image
# without errors.
#
# Commands:
#   docker build -t quizapp-pipeline:latest .
#   docker images quizapp-pipeline
#
# ✅ Pass criteria:
#   [ ] Build completes with no errors
#   [ ] Image appears in "docker images" output
#   [ ] Image size is under 200 MB (slim base + no dev deps)
#   [ ] Multi-stage build used (no compilers in final image)
#   [ ] No secrets or .env file baked into the image
#
# Verify no secrets leaked into the image:
#   docker run --rm quizapp-pipeline:latest cat /app/.env
#   → Should fail with "No such file or directory"
#
#   docker run --rm quizapp-pipeline:latest ls /app/instance/
#   → Should show empty directory (DB created at runtime)


# ════════════════════════════════════════════════════════════
# 2. CONTAINER STARTS SUCCESSFULLY
# ════════════════════════════════════════════════════════════
#
# Verifies the container boots, Flask initializes, and the
# database is seeded without crashes.
#
# Commands:
#   docker compose up -d --build
#   docker compose ps
#   docker compose logs web
#
# ✅ Pass criteria:
#   [ ] Container status shows "Up" (not "Restarting" or "Exited")
#   [ ] Health check shows "healthy" (after ~30 seconds)
#   [ ] Logs show "Running on http://0.0.0.0:5000"
#   [ ] Logs show database tables created (no SQLAlchemy errors)
#   [ ] Logs show seed data inserted (admin user, categories)
#   [ ] No Python tracebacks in the logs
#
# Check health status:
#   docker inspect --format='{{.State.Health.Status}}' quizapp_web
#   → Should return "healthy"


# ════════════════════════════════════════════════════════════
# 3. WEBSITE OPENS IN BROWSER
# ════════════════════════════════════════════════════════════
#
# Verifies the application is reachable from the host machine.
#
# Action:
#   Open http://localhost:5000 in your browser
#
# ✅ Pass criteria:
#   [ ] Page loads without connection errors
#   [ ] Redirects to login page (or dashboard if logged in)
#   [ ] CSS and Bootstrap styles render correctly
#   [ ] No broken images or missing static assets
#   [ ] JavaScript loads (check browser DevTools console for errors)
#   [ ] Page is responsive (resize browser window)
#
# Quick command-line test:
#   curl -sI http://localhost:5000
#   → Should return HTTP 302 (redirect to login)


# ════════════════════════════════════════════════════════════
# 4. USER AUTHENTICATION WORKS
# ════════════════════════════════════════════════════════════
#
# Verifies registration, login, logout, and session management.
#
# Actions:
#
# 4a. Admin Login
#   [ ] Navigate to http://localhost:5000/auth/login
#   [ ] Enter: admin@quizapp.com / Admin@123
#   [ ] Click "Login"
#   [ ] Verify redirect to dashboard
#   [ ] Verify admin navigation links are visible
#
# 4b. New User Registration
#   [ ] Navigate to http://localhost:5000/auth/register
#   [ ] Fill in: Full Name, Email, Password, Confirm Password
#   [ ] Click "Register"
#   [ ] Verify redirect to login page with success message
#
# 4c. New User Login
#   [ ] Login with the newly registered credentials
#   [ ] Verify redirect to dashboard
#   [ ] Verify admin links are NOT visible (regular user)
#
# 4d. Logout
#   [ ] Click "Logout"
#   [ ] Verify redirect to login page
#   [ ] Attempt to access /main/dashboard directly
#   [ ] Verify redirect back to login (session cleared)
#
# 4e. CSRF Protection
#   [ ] Inspect any form in DevTools → confirm hidden csrf_token field exists
#   [ ] Attempt to POST without CSRF token → should be rejected


# ════════════════════════════════════════════════════════════
# 5. QUIZ SYSTEM WORKS
# ════════════════════════════════════════════════════════════
#
# Verifies the core quiz-taking flow end-to-end.
#
# Actions:
#   [ ] Login as a regular user
#   [ ] Navigate to quiz selection (choose a category)
#   [ ] Verify questions load with 4 options each
#   [ ] Verify countdown timer starts and is visible
#   [ ] Select answers for all questions
#   [ ] Submit the quiz
#   [ ] Verify results page shows:
#       - Score (e.g., 3/5)
#       - Percentage
#       - Pass/Fail indicator
#       - Question-by-question review with correct answers
#   [ ] Navigate to attempt history
#   [ ] Verify the completed quiz appears in the history log


# ════════════════════════════════════════════════════════════
# 6. DATABASE PERSISTENCE
# ════════════════════════════════════════════════════════════
#
# Verifies that data survives container restarts and rebuilds.
# This is critical – if the volume isn't working, all data
# is lost on every restart.
#
# Actions:
#
# 6a. Register a test user and take a quiz (create data)
#
# 6b. Restart the container:
#   docker compose restart web
#   → Wait for "healthy" status
#
#   [ ] Login with the test user → succeeds
#   [ ] Previous quiz attempt appears in history
#
# 6c. Rebuild the container (simulates code update):
#   docker compose down
#   docker compose up -d --build
#   → Wait for "healthy" status
#
#   [ ] Login with the test user → succeeds
#   [ ] Previous quiz attempt STILL appears in history
#   [ ] Admin user still exists
#   [ ] All categories still exist
#
# 6d. Verify volume exists:
#   docker volume ls | grep quizapp_sqlite_data
#   → Should show the named volume
#
#   docker volume inspect quizapp_sqlite_data
#   → Should show Mountpoint path on host


# ════════════════════════════════════════════════════════════
# 7. ADMIN PANEL WORKS
# ════════════════════════════════════════════════════════════
#
# Verifies all administrative CRUD operations.
#
# Actions (login as admin@quizapp.com):
#
# 7a. Category Management
#   [ ] View all categories
#   [ ] Create a new category (e.g., "Linux")
#   [ ] Verify new category appears in the list
#   [ ] Delete the test category
#   [ ] Verify it is removed
#
# 7b. Question Management
#   [ ] View all questions (with category filter)
#   [ ] Add a new question to an existing category
#   [ ] Edit an existing question (change text/options)
#   [ ] Delete a question
#   [ ] Verify changes persist after page refresh
#
# 7c. User Management
#   [ ] View all registered users
#   [ ] Verify user details are displayed (name, email, role, date)
#
# 7d. Scores / Attempts Log
#   [ ] View all quiz attempts across all users
#   [ ] Verify scores, percentages, and dates are correct
#
# 7e. Access Control
#   [ ] Login as a regular user
#   [ ] Attempt to access /admin/ routes directly
#   [ ] Verify access is denied (redirect or 403)


# ════════════════════════════════════════════════════════════
# 8. CI/CD PIPELINE PASSES
# ════════════════════════════════════════════════════════════
#
# Verifies the GitHub Actions workflow runs successfully.
#
# Actions:
#   [ ] Push code to GitHub (main or develop branch)
#   [ ] Navigate to repo → "Actions" tab
#   [ ] Verify the "CI/CD Quiz App Pipeline" workflow triggers
#   [ ] Verify all 3 stages pass:
#       [ ] 🔍 Lint   – flake8 finds no syntax errors
#       [ ] 🧪 Test   – all unit tests pass
#       [ ] 🐳 Docker – image builds, container starts, HTTP 200/302
#   [ ] Open a Pull Request → verify checks appear on the PR
#
# If a stage fails:
#   - Click the failed job → expand the failed step
#   - Read the error output
#   - Fix locally → push again


# ════════════════════════════════════════════════════════════
# 9. PRODUCTION READINESS FINAL CHECK
# ════════════════════════════════════════════════════════════
#
# Security & configuration hardening before going live.
#
# ✅ Pass criteria:
#
# Security:
#   [ ] SECRET_KEY is a strong random value (not the default)
#       → python -c "import secrets; print(secrets.token_hex(32))"
#   [ ] ADMIN_PASSWORD has been changed from "Admin@123"
#   [ ] FLASK_DEBUG is set to False
#   [ ] FLASK_ENV is set to "production"
#   [ ] .env file is NOT committed to Git
#       → git status should NOT show .env
#   [ ] Container runs as non-root user (appuser)
#       → docker exec quizapp_web whoami → "appuser"
#
# Files:
#   [ ] .gitignore is comprehensive and tested
#   [ ] .dockerignore excludes secrets, venv, and test files
#   [ ] .env.example is committed (safe template)
#   [ ] README.md is complete with setup instructions
#
# Infrastructure:
#   [ ] Named volume is configured for SQLite persistence
#   [ ] Restart policy is "unless-stopped"
#   [ ] Healthcheck is configured and reporting "healthy"
#   [ ] Log rotation is configured (max 10m × 3 files)
#   [ ] Resource limits are set (256 MB RAM, 0.50 CPU)
#
# CI/CD:
#   [ ] GitHub Actions pipeline passes on main branch
#   [ ] Pipeline runs on both push and pull_request
#   [ ] All 3 stages (lint, test, docker) are green


# ════════════════════════════════════════════════════════════
# SUMMARY – VERIFICATION COMMANDS (QUICK RUN)
# ════════════════════════════════════════════════════════════
#
# Run these in order for a rapid smoke test:
#
#   # Build and start
#   docker compose up -d --build
#
#   # Wait for healthy
#   sleep 15
#   docker inspect --format='{{.State.Health.Status}}' quizapp_web
#
#   # Check container status
#   docker compose ps
#
#   # Test HTTP response
#   curl -sI http://localhost:5000
#
#   # Verify non-root user
#   docker exec quizapp_web whoami
#
#   # Check logs for errors
#   docker compose logs --tail 30 web
#
#   # Verify volume exists
#   docker volume ls | grep quizapp
#
#   # Check image size
#   docker images quizapp-pipeline --format "{{.Size}}"
#
# All green? 🎉 Your application is production-ready!
