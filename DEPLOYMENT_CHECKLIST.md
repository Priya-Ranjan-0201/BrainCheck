# ============================================================
# Deployment Verification Checklist
# Dockerized Quiz Application
# ============================================================
#
# This checklist ensures every component of the application
# is functioning correctly before declaring it production-ready.
#
# Instructions:
#   1. Work through each section in order
#   2. Run the commands and verify the expected outcomes
#   3. Mark each item as [x] when verified
#   4. If any item fails, check the Troubleshooting section
#      at the bottom of this document
#
# Prerequisites:
#   • Docker Desktop installed and running
#   • Terminal open in the project root (Dockerized-Quiz-App/)
#   • .env file configured with your settings
#
# Estimated time: 15-20 minutes
# ============================================================


# ════════════════════════════════════════════════════════════
# 1. DOCKER IMAGE BUILD
# ════════════════════════════════════════════════════════════
#
# Verifies the Dockerfile produces a valid, optimized image.
#
# ── Commands ────────────────────────────────────────────────

docker build -t quizapp-pipeline:latest .
docker images quizapp-pipeline

# ── Verification items ──────────────────────────────────────
#
# [ ] Build completes with "Successfully built" message
#     → If not: read the error output. Common issues:
#       • requirements.txt has a typo in a package name
#       • Dockerfile syntax error
#       • Network issue downloading base image
#
# [ ] Image appears in "docker images" output
#     → Look for REPOSITORY "quizapp-pipeline" with TAG "latest"
#
# [ ] Image size is under 200 MB
#     → Check the SIZE column. Expected: ~140-170 MB
#     → If larger: .dockerignore may not be excluding venv/
#
# [ ] Multi-stage build is working (no build tools in final image)
#     → Verify: docker run --rm quizapp-pipeline:latest dpkg -l | grep build-essential
#     → Expected: no output (build-essential is not installed)
#
# [ ] No secrets leaked into the image
#     → Verify: docker run --rm quizapp-pipeline:latest cat /app/.env 2>&1
#     → Expected: "No such file or directory" error
#
# [ ] Non-root user is configured
#     → Verify: docker run --rm quizapp-pipeline:latest whoami
#     → Expected: "appuser"
#
# [ ] Instance directory exists and is writable
#     → Verify: docker run --rm quizapp-pipeline:latest ls -la /app/instance/
#     → Expected: directory owned by appuser:appgroup


# ════════════════════════════════════════════════════════════
# 2. CONTAINER STARTS SUCCESSFULLY
# ════════════════════════════════════════════════════════════
#
# Verifies the container boots, Flask initializes, the
# database is created, and seed data is inserted.
#
# ── Commands ────────────────────────────────────────────────

docker compose up -d --build
sleep 15  # Wait for startup and health check
docker compose ps
docker compose logs --tail 30 web

# ── Verification items ──────────────────────────────────────
#
# [ ] "docker compose ps" shows STATUS as "Up" (not "Exited" or "Restarting")
#     → If "Exited (1)": check logs for Python tracebacks
#     → If "Restarting": the app is crash-looping — check logs
#
# [ ] Health check shows "(healthy)" in the STATUS column
#     → Verify: docker inspect --format='{{.State.Health.Status}}' quizapp_web
#     → Expected: "healthy"
#     → If "unhealthy": Flask didn't start — check logs
#     → Note: Health check starts after 15s, runs every 30s
#
# [ ] Logs show Flask startup message:
#     "* Serving Flask app 'app'"
#     "* Running on http://0.0.0.0:5000"
#
# [ ] Logs show database initialization (no SQLAlchemy errors)
#     → Look for: no "OperationalError" or "sqlite3" error messages
#
# [ ] Logs show seed data was inserted
#     → On first run, admin user and sample categories are created
#     → No explicit log message, but absence of errors confirms success
#
# [ ] No Python tracebacks in the logs
#     → Search: docker compose logs web 2>&1 | findstr "Traceback"
#     → Expected: no output
#
# [ ] Container runs as non-root user
#     → Verify: docker exec quizapp_web whoami
#     → Expected: "appuser"


# ════════════════════════════════════════════════════════════
# 3. WEBSITE OPENS IN BROWSER
# ════════════════════════════════════════════════════════════
#
# Verifies the application is reachable from the host machine
# and renders correctly in the browser.
#
# ── Action ──────────────────────────────────────────────────
#
# Open http://localhost:5000 in your web browser.
#
# ── Quick command-line test ─────────────────────────────────

curl -sI http://localhost:5000

# Expected HTTP response:
#   HTTP/1.1 302 FOUND
#   Location: /auth/login
# (Root redirects to login page for unauthenticated users)

# ── Verification items ──────────────────────────────────────
#
# [ ] Page loads without connection errors (no ERR_CONNECTION_REFUSED)
#     → If refused: container may not be running or port isn't mapped
#
# [ ] Browser shows the login page (redirected from /)
#     → Should see a styled login form with email and password fields
#
# [ ] CSS renders correctly (Bootstrap 5 styling is visible)
#     → Cards have borders, buttons are colored, fonts are correct
#     → If unstyled: static files aren't being served — check logs
#
# [ ] No broken images or missing static assets
#     → Open browser DevTools → Network tab → filter by "4xx"
#     → Expected: no 404 errors for CSS, JS, or image files
#
# [ ] JavaScript loads without errors
#     → Open browser DevTools → Console tab
#     → Expected: no red error messages
#
# [ ] Page is responsive (mobile-friendly)
#     → Resize browser to phone width (~375px)
#     → Expected: layout adjusts, no horizontal scrolling
#
# [ ] HTTPS redirect works (if configured)
#     → Only applicable if you've set up SSL/TLS


# ════════════════════════════════════════════════════════════
# 4. USER AUTHENTICATION WORKS
# ════════════════════════════════════════════════════════════
#
# Verifies registration, login, logout, and session security.
#
# ── 4a. Admin Login ─────────────────────────────────────────
#
# [ ] Navigate to http://localhost:5000/auth/login
# [ ] Enter email: admin@quizapp.com
# [ ] Enter password: Admin@123
# [ ] Click "Login" button
# [ ] Verify: redirected to the dashboard
# [ ] Verify: admin navigation links are visible (Admin Panel, etc.)
# [ ] Verify: dashboard shows statistics cards
# [ ] Verify: the performance chart canvas renders
#
# ── 4b. New User Registration ──────────────────────────────
#
# [ ] Click "Logout" (if logged in)
# [ ] Navigate to http://localhost:5000/auth/register
# [ ] Fill in:
#     • Full Name: Test Student
#     • Email: student@test.com
#     • Password: TestPassword123
#     • Confirm Password: TestPassword123
# [ ] Click "Register" button
# [ ] Verify: redirected to login page with success flash message
#     → "Registration successful! Please log in."
#
# ── 4c. New User Login ─────────────────────────────────────
#
# [ ] Enter email: student@test.com
# [ ] Enter password: TestPassword123
# [ ] Click "Login" button
# [ ] Verify: redirected to dashboard
# [ ] Verify: admin navigation links are NOT visible (regular user)
# [ ] Verify: dashboard is accessible and shows empty stats
#
# ── 4d. Logout Flow ────────────────────────────────────────
#
# [ ] Click "Logout" button/link
# [ ] Verify: redirected to login page
# [ ] Attempt to navigate directly to http://localhost:5000/dashboard/
# [ ] Verify: redirected back to login with message:
#     → "Please log in to access this page."
#
# ── 4e. Invalid Login ──────────────────────────────────────
#
# [ ] Attempt login with wrong password
# [ ] Verify: error message "Invalid email or password."
# [ ] Attempt login with non-existent email
# [ ] Verify: same error message (doesn't reveal which field is wrong)
#
# ── 4f. Duplicate Registration ─────────────────────────────
#
# [ ] Attempt to register with admin@quizapp.com (existing email)
# [ ] Verify: error message about email already being registered
#
# ── 4g. CSRF Protection ───────────────────────────────────
#
# [ ] Inspect any form in DevTools → look for a hidden input:
#     <input type="hidden" name="csrf_token" value="...">
# [ ] Verify the token exists and is populated


# ════════════════════════════════════════════════════════════
# 5. QUIZ SYSTEM WORKS END-TO-END
# ════════════════════════════════════════════════════════════
#
# Verifies the complete quiz flow: category selection →
# question delivery → answer submission → scoring → history.
#
# ── Prerequisites: Login as student@test.com ────────────────
#
# ── 5a. Category Selection ─────────────────────────────────
#
# [ ] Navigate to quiz categories page
# [ ] Verify: all 4 seeded categories appear:
#     Python, JavaScript, Docker, General Knowledge
# [ ] Each category card shows question count
# [ ] Click on "Python" category to start
#
# ── 5b. Quiz Taking ───────────────────────────────────────
#
# [ ] Questions load one-at-a-time with 4 radio button options
# [ ] Questions appear in a randomized order
# [ ] Countdown timer is visible and counting down from 5:00
# [ ] Timer changes color/style when time is running low
# [ ] Selecting an option highlights it visually
# [ ] Previously selected option is retained on the page
# [ ] All 5 Python questions are presented
#
# ── 5c. Quiz Submission ───────────────────────────────────
#
# [ ] Click "Submit Quiz" button after answering all questions
# [ ] Verify: redirected to the results page
#
# ── 5d. Results Page ──────────────────────────────────────
#
# [ ] Score is displayed (e.g., "3 out of 5")
# [ ] Percentage is calculated correctly
# [ ] Pass/Fail indicator is shown
# [ ] Question-by-question review is displayed:
#     • Question text
#     • Your answer (highlighted)
#     • Correct answer (highlighted in green)
#     • Visual indicator for correct/incorrect
#
# ── 5e. Attempt History ──────────────────────────────────
#
# [ ] Navigate to attempt history page
# [ ] Verify: the quiz you just completed appears in the list
# [ ] Verify: correct details shown:
#     • Category name (Python)
#     • Score (e.g., 3/5)
#     • Percentage
#     • Date/time of completion
# [ ] Take another quiz (e.g., Docker) and verify it appears too


# ════════════════════════════════════════════════════════════
# 6. DATABASE PERSISTENCE ACROSS RESTARTS
# ════════════════════════════════════════════════════════════
#
# This is the most critical verification. If the named volume
# isn't working correctly, ALL data is lost every time the
# container restarts or is rebuilt.
#
# ── 6a. Verify volume exists ───────────────────────────────

docker volume ls | findstr quiz
# Expected: "local    quizapp_sqlite_data"

docker volume inspect quizapp_sqlite_data
# Shows the Mountpoint path on the host filesystem

# ── 6b. Test persistence across restart ────────────────────
#
# Prerequisites: You should have registered student@test.com
# and completed at least one quiz in Step 5.

docker compose restart web

# Wait for healthy:
sleep 15
docker inspect --format='{{.State.Health.Status}}' quizapp_web
# Expected: "healthy"

# [ ] Login with student@test.com → succeeds
# [ ] Dashboard shows previous quiz statistics
# [ ] Attempt history shows the quiz(zes) taken earlier
# [ ] Admin login (admin@quizapp.com) still works
# [ ] All 4 categories still exist
#
# ── 6c. Test persistence across rebuild ────────────────────
#
# This simulates deploying a code update — the container is
# completely destroyed and recreated, but the volume survives.

docker compose down
docker compose up -d --build

# Wait for healthy:
sleep 15
docker inspect --format='{{.State.Health.Status}}' quizapp_web
# Expected: "healthy"

# [ ] Login with student@test.com → STILL succeeds
# [ ] Previous quiz attempts are STILL in history
# [ ] Admin user STILL exists with same credentials
# [ ] All categories and questions STILL exist
# [ ] New data can be added (take another quiz)
#
# ── 6d. Verify data is in the volume (not the container) ───

# Check database file in the container:
docker exec quizapp_web ls -la /app/instance/database.db
# Expected: file exists with non-zero size

# Check volume on host:
docker volume inspect quizapp_sqlite_data --format='{{.Mountpoint}}'
# Note the path — this is where Docker stores the database


# ════════════════════════════════════════════════════════════
# 7. ADMIN PANEL WORKS
# ════════════════════════════════════════════════════════════
#
# Verifies all administrative CRUD operations and access control.
#
# ── Login as admin@quizapp.com / Admin@123 ──────────────────
#
# ── 7a. Admin Dashboard ───────────────────────────────────
#
# [ ] Navigate to /admin/ (or click Admin Panel link)
# [ ] Verify: summary statistics cards are displayed:
#     • Total Users count
#     • Total Categories count
#     • Total Questions count
#     • Total Attempts count
# [ ] Verify: quick-navigation cards/links to all admin views
#
# ── 7b. Category Management ──────────────────────────────
#
# [ ] Navigate to category management page
# [ ] Verify: all 4 seeded categories are listed
# [ ] Create a new category: Enter "Linux" → click Create
# [ ] Verify: "Linux" appears in the category list
# [ ] Verify: success flash message is displayed
# [ ] Delete the "Linux" category → click Delete
# [ ] Verify: "Linux" is removed from the list
# [ ] Verify: success flash message confirms deletion
# [ ] Verify: attempting to delete a category with questions
#     shows a warning or cascading-deletes the questions
#
# ── 7c. Question Management ─────────────────────────────
#
# [ ] Navigate to questions management page
# [ ] Verify: all seeded questions are listed
# [ ] Verify: category filter works (select "Python" → only Python questions shown)
#
# [ ] ADD a new question:
#     • Select category: Docker
#     • Question: "What is Docker Hub?"
#     • Option A: "A container registry"
#     • Option B: "A programming language"
#     • Option C: "An operating system"
#     • Option D: "A text editor"
#     • Correct: A
#     • Click "Add Question"
# [ ] Verify: new question appears in the list
# [ ] Verify: success flash message is displayed
#
# [ ] EDIT an existing question:
#     • Click "Edit" on the question you just created
#     • Change the question text slightly
#     • Click "Update"
# [ ] Verify: changes are saved and reflected in the list
#
# [ ] DELETE a question:
#     • Click "Delete" on the question you created
# [ ] Verify: question is removed from the list
# [ ] Verify: changes persist after page refresh (F5)
#
# ── 7d. User Directory ──────────────────────────────────
#
# [ ] Navigate to user management page
# [ ] Verify: admin user (admin@quizapp.com) is listed
# [ ] Verify: test student (student@test.com) is listed
# [ ] Verify: user details shown: full name, email, role, registration date
# [ ] Verify: admin has role "admin", student has role "user"
#
# ── 7e. Scores / Attempts Log ──────────────────────────
#
# [ ] Navigate to attempts log page
# [ ] Verify: quiz attempts from Step 5 are listed
# [ ] Verify: details shown: user name, category, score, percentage, date
# [ ] Verify: scores and percentages are mathematically correct
#
# ── 7f. Access Control ─────────────────────────────────
#
# [ ] Logout from admin account
# [ ] Login as student@test.com (regular user)
# [ ] Attempt to navigate directly to:
#     • http://localhost:5000/admin/
#     • http://localhost:5000/admin/categories
#     • http://localhost:5000/admin/users
# [ ] Verify: access is denied (redirect to dashboard or 403 error)
# [ ] Verify: admin links are NOT visible in the navigation bar


# ════════════════════════════════════════════════════════════
# 8. CI/CD PIPELINE PASSES
# ════════════════════════════════════════════════════════════
#
# Verifies the GitHub Actions workflow executes successfully.
#
# ── Prerequisites ───────────────────────────────────────────
# Code must be pushed to GitHub (see GITHUB_SETUP.md)
#
# ── Verification items ──────────────────────────────────────
#
# [ ] Push code to GitHub (main or develop branch):
#     git push origin main
#
# [ ] Navigate to your GitHub repository → "Actions" tab
#
# [ ] Verify the "CI/CD Quiz App Pipeline" workflow was triggered
#     → Should show as "In progress" or "Queued"
#
# [ ] Verify all 3 stages pass:
#
#     [ ] 🔍 Lint (flake8)
#         → No Python syntax errors
#         → No undefined variable names
#         → Style warnings are logged but don't block
#
#     [ ] 🧪 Test (unittest)
#         → All 6 test cases pass
#         → Test output shows "OK" at the end
#         → Tests run against an in-memory SQLite database
#
#     [ ] 🐳 Docker Build
#         → Image builds successfully
#         → Container starts without crashing
#         → HTTP health check returns 200 or 302
#         → Container logs are printed (even on failure)
#         → Test container is cleaned up
#
# [ ] Open a Pull Request → verify CI checks appear on the PR
#     → Status checks should show green checkmarks
#
# ── If a stage fails ───────────────────────────────────────
#
#   1. Click the failed job name in the Actions tab
#   2. Expand the failed step (red ❌ icon)
#   3. Read the error output
#   4. Fix the issue locally
#   5. Commit and push again
#   6. The pipeline re-runs automatically


# ════════════════════════════════════════════════════════════
# 9. PRODUCTION READINESS — SECURITY & CONFIGURATION
# ════════════════════════════════════════════════════════════
#
# Final hardening checks before declaring production-ready.
#
# ── Security Checklist ──────────────────────────────────────
#
# [ ] SECRET_KEY is a strong random value (NOT the default)
#     → Generate: python -c "import secrets; print(secrets.token_hex(32))"
#     → Paste into .env
#     → Verify it's not "quiz-app-super-secret-key-change-me"
#
# [ ] ADMIN_PASSWORD has been changed from "Admin@123"
#     → Set a strong password in .env
#     → Delete the container and database, then rebuild to
#       re-seed with the new password
#
# [ ] FLASK_DEBUG is set to False
#     → Check .env: FLASK_DEBUG=False
#     → Verify: docker exec quizapp_web env | findstr FLASK_DEBUG
#     → Why: debug mode exposes a Werkzeug debugger that allows
#       arbitrary Python code execution
#
# [ ] FLASK_ENV is set to "production"
#     → Check .env: FLASK_ENV=production
#
# [ ] .env file is NOT committed to Git
#     → Verify: git ls-files .env (should return nothing)
#     → Verify: .env is listed in .gitignore
#
# [ ] .env.example IS committed (safe template for collaborators)
#     → Verify: git ls-files .env.example (should return the file)
#
# [ ] Container runs as non-root user
#     → Verify: docker exec quizapp_web whoami → "appuser"
#     → Why: if the app is compromised, the attacker has
#       limited privileges
#
# [ ] CSRF protection is enabled
#     → Check config.py: WTF_CSRF_ENABLED = True
#     → Inspect any form in DevTools: csrf_token field exists
#
# [ ] SESSION_COOKIE_HTTPONLY is True
#     → Prevents JavaScript from reading session cookies
#
# [ ] SESSION_COOKIE_SAMESITE is "Lax" or "Strict"
#     → Prevents CSRF attacks via cross-site requests
#
# ── File Checklist ──────────────────────────────────────────
#
# [ ] .gitignore is comprehensive (ignores venv, *.db, .env, etc.)
# [ ] .dockerignore excludes secrets, venv, tests, and git history
# [ ] .env.example contains all variables with safe placeholder values
# [ ] README.md is complete with setup instructions and architecture
# [ ] All documentation files are present and accurate
#
# ── Infrastructure Checklist ────────────────────────────────
#
# [ ] Named volume "quizapp_sqlite_data" is configured
#     → Verify: docker volume ls | findstr quiz
#
# [ ] Restart policy is "unless-stopped"
#     → Verify: docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' quizapp_web
#     → Expected: "unless-stopped"
#
# [ ] Healthcheck is configured and passing
#     → Verify: docker inspect --format='{{.State.Health.Status}}' quizapp_web
#     → Expected: "healthy"
#
# [ ] Log rotation is configured (docker-compose.yml)
#     → max-size: "10m", max-file: "3"
#     → Prevents disk exhaustion on long-running deployments
#
# [ ] Resource limits are set (docker-compose.yml)
#     → Memory limit: 256 MB
#     → CPU limit: 0.50
#     → Prevents a runaway process from consuming all host resources
#
# ── CI/CD Checklist ─────────────────────────────────────────
#
# [ ] GitHub Actions pipeline passes on main branch
# [ ] Pipeline runs on both push and pull_request events
# [ ] All 3 stages (lint, test, docker) show green checkmarks
# [ ] Branch protection rules are configured (optional but recommended)


# ════════════════════════════════════════════════════════════
# QUICK SMOKE TEST — RUN IN ORDER
# ════════════════════════════════════════════════════════════
#
# A rapid 10-command sequence to validate the entire
# deployment in under 2 minutes:

# 1. Build and start
docker compose up -d --build

# 2. Wait for startup
sleep 15

# 3. Check health status
docker inspect --format='{{.State.Health.Status}}' quizapp_web

# 4. Check container status
docker compose ps

# 5. Test HTTP response
curl -sI http://localhost:5000

# 6. Verify non-root execution
docker exec quizapp_web whoami

# 7. Check for errors in logs
docker compose logs --tail 10 web

# 8. Verify volume exists
docker volume ls | findstr quiz

# 9. Check image size
docker images quizapp-pipeline --format "{{.Size}}"

# 10. Verify .env is not tracked
# git ls-files .env

# ── Expected Results ────────────────────────────────────────
#
#   Step 3: "healthy"
#   Step 4: STATUS shows "Up" with "(healthy)"
#   Step 5: HTTP/1.1 302 FOUND
#   Step 6: "appuser"
#   Step 7: No tracebacks, shows Flask startup
#   Step 8: Shows "quizapp_sqlite_data"
#   Step 9: ~140-170 MB
#   Step 10: No output (properly ignored)
#
# All green? 🎉 Your application is production-ready!


# ════════════════════════════════════════════════════════════
# TROUBLESHOOTING
# ════════════════════════════════════════════════════════════
#
# ── Container won't start / exits immediately ──────────────
#   1. docker compose logs web
#   2. Look for ImportError, ModuleNotFoundError, or syntax errors
#   3. Fix the issue in code → docker compose up -d --build
#
# ── "Port already in use" error ────────────────────────────
#   1. Find what's using port 5000:
#      netstat -ano | findstr :5000     (PowerShell)
#   2. Change PORT in .env to 8080 (or another free port)
#   3. docker compose up -d --force-recreate
#
# ── Database is empty after restart ────────────────────────
#   1. Check if volume exists: docker volume ls | findstr quiz
#   2. Check docker-compose.yml has the volume mount
#   3. Ensure DATABASE_URL uses /app/instance/ path
#
# ── Health check fails ("unhealthy") ──────────────────────
#   1. docker compose logs --tail 50 web
#   2. Try manually: docker exec quizapp_web python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"
#   3. If Flask isn't starting, fix the app error first
#
# ── CSS/JS not loading (unstyled page) ────────────────────
#   1. Check browser DevTools → Network tab for 404s
#   2. Verify static/ directory is in the Docker image:
#      docker exec quizapp_web ls -la /app/static/
#   3. Check .dockerignore isn't excluding static/
#
# ── Permission denied errors ──────────────────────────────
#   1. Rebuild from scratch: docker compose build --no-cache
#   2. Verify instance/ ownership:
#      docker exec quizapp_web ls -la /app/instance/
#      → Should be owned by appuser:appgroup
