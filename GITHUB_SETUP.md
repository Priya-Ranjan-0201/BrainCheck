# ============================================================
# GitHub Repository Preparation Guide
# Dockerized Quiz Application
# ============================================================
#
# This guide walks you through cleaning up the project,
# initializing Git, crafting a commit strategy, pushing to
# GitHub, and setting up branches and release tags.
#
# Prerequisites:
#   • Git installed  →  https://git-scm.com/downloads
#   • GitHub account →  https://github.com
#   • Terminal open in the project root (Dockerized-Quiz-App/)
# ============================================================


# ─────────────────────────────────────────────────────────────
# STEP 1: FOLDER CLEANUP
# ─────────────────────────────────────────────────────────────
#
# Before your first commit, remove any files that should NOT
# be in the repository. The .gitignore will prevent them from
# being tracked going forward, but existing files must be
# cleaned up manually first.
#
# Checklist:
#
#   ✅ Delete __pycache__/ directories
#   ✅ Delete .venv/ or venv/ (virtual environment)
#   ✅ Delete instance/*.db (SQLite database files)
#   ✅ Delete *.pyc compiled bytecode files
#   ✅ Delete .pytest_cache/ if present
#   ✅ Ensure .env is NOT committed (secrets!)
#   ✅ Keep .env.example (safe template for collaborators)
#   ✅ Remove any IDE workspace files (.vscode/, .idea/)
#
# Run these cleanup commands (PowerShell):

# Remove Python cache folders:
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Remove virtual environment (if present at project root):
if (Test-Path ".venv") { Remove-Item -Recurse -Force ".venv" }
if (Test-Path "venv")  { Remove-Item -Recurse -Force "venv"  }

# Remove compiled bytecode:
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force

# Remove SQLite database files from instance/:
if (Test-Path "instance") { Get-ChildItem "instance" -Filter "*.db" | Remove-Item -Force }

# Remove pytest cache:
if (Test-Path ".pytest_cache") { Remove-Item -Recurse -Force ".pytest_cache" }


# ─────────────────────────────────────────────────────────────
# STEP 2: VERIFY PROJECT STRUCTURE
# ─────────────────────────────────────────────────────────────
#
# After cleanup, your project should look like this:
#
#   Dockerized-Quiz-App/
#   ├── .dockerignore
#   ├── .env                    ← NOT committed (in .gitignore)
#   ├── .env.example            ← Committed (safe template)
#   ├── .github/
#   │   └── workflows/
#   │       └── docker-ci.yml   ← CI/CD pipeline (Step 9)
#   ├── .gitignore
#   ├── Dockerfile
#   ├── DOCKER_COMMANDS.md
#   ├── DOCKER_COMPOSE_COMMANDS.md
#   ├── README.md
#   ├── app.py
#   ├── config.py
#   ├── docker-compose.yml
#   ├── models/
#   │   ├── __init__.py
#   │   └── models.py
#   ├── requirements.txt
#   ├── routes/
#   │   ├── __init__.py
#   │   ├── admin.py
#   │   ├── auth.py
#   │   ├── main.py
#   │   └── quiz.py
#   ├── static/
#   │   ├── css/style.css
#   │   └── js/main.js
#   ├── templates/
#   │   ├── base.html
#   │   ├── admin/
#   │   ├── auth/
#   │   ├── main/
#   │   └── quiz/
#   └── tests/
#       ├── __init__.py
#       └── test_app.py
#
# Confirm with:
Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch '\\(\.venv|venv|__pycache__|\.git)\\' } | Select-Object FullName


# ─────────────────────────────────────────────────────────────
# STEP 3: INITIALIZE THE GIT REPOSITORY
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Creates a hidden .git/ directory that tracks all changes.
#   The -b flag sets the default branch name to "main"
#   (industry standard, replacing the legacy "master").

git init -b main


# ─────────────────────────────────────────────────────────────
# STEP 4: CONFIGURE GIT IDENTITY
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Sets your name and email for commit authorship.
#   Use the same email linked to your GitHub account.
#
#   --global  →  Applies to all repos on this machine
#   (omit --global to set per-repo only)

git config --global user.name "PRIYE RANJAN"
git config --global user.email "your-email@example.com"


# ─────────────────────────────────────────────────────────────
# STEP 5: COMMIT STRATEGY
# ─────────────────────────────────────────────────────────────
#
# Use atomic, well-described commits grouped by logical phase.
# This creates a clean, professional Git history.
#
# Commit message format (Conventional Commits):
#
#   <type>(<scope>): <short description>
#
#   Types:
#     feat     →  New feature
#     fix      →  Bug fix
#     docs     →  Documentation only
#     style    →  Formatting, no logic change
#     refactor →  Code restructuring
#     test     →  Adding or updating tests
#     ci       →  CI/CD pipeline changes
#     chore    →  Build, tooling, or config changes
#
# ─────────────────────────────────────────────────────────────

# ── Commit 1: Core Application ──────────────────────────────
# Stage the Flask app, models, routes, config, and dependencies.

git add app.py config.py requirements.txt
git add models/ routes/
git commit -m "feat(app): add Flask application with auth, quiz engine, and admin panel"

# ── Commit 2: Frontend ──────────────────────────────────────
# Stage templates and static assets.

git add templates/ static/
git commit -m "feat(ui): add Bootstrap 5 templates and interactive JS components"

# ── Commit 3: Tests ─────────────────────────────────────────
# Stage the test suite.

git add tests/
git commit -m "test(app): add unit test suite for core application features"

# ── Commit 4: Docker Configuration ──────────────────────────
# Stage all Docker-related files.

git add Dockerfile docker-compose.yml .dockerignore
git commit -m "chore(docker): add multi-stage Dockerfile and Compose orchestration"

# ── Commit 5: Environment & Git Config ──────────────────────
# Stage .gitignore and the safe .env template.

git add .gitignore .env.example
git commit -m "chore(config): add .gitignore and .env.example template"

# ── Commit 6: Documentation ─────────────────────────────────
# Stage README and Docker command guides.

git add README.md DOCKER_COMMANDS.md DOCKER_COMPOSE_COMMANDS.md
git commit -m "docs: add README, Docker build guide, and Compose commands reference"

# ── Commit 7: CI/CD Pipeline ────────────────────────────────
# Stage the GitHub Actions workflow (generated in Step 9).

git add .github/
git commit -m "ci(github-actions): add Docker build and test validation pipeline"


# ─────────────────────────────────────────────────────────────
# STEP 6: CREATE THE GITHUB REPOSITORY
# ─────────────────────────────────────────────────────────────
#
# Option A: GitHub Web UI
#   1. Go to https://github.com/new
#   2. Repository name: Dockerized-Quiz-App
#   3. Description: Production-ready Flask Quiz Application
#                    with Docker & CI/CD
#   4. Visibility: Public (or Private)
#   5. Do NOT initialize with README, .gitignore, or license
#      (we already have these locally)
#   6. Click "Create repository"
#
# Option B: GitHub CLI (if installed)
#   gh repo create Dockerized-Quiz-App --public --source=. --remote=origin


# ─────────────────────────────────────────────────────────────
# STEP 7: CONNECT & PUSH TO GITHUB
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Links your local repository to the remote GitHub repo
#   and pushes all commits.
#
#   -u  →  Sets "origin main" as the default upstream, so
#          future pushes only need "git push".
#
# Replace <your-username> with your actual GitHub username.

git remote add origin https://github.com/<your-username>/Dockerized-Quiz-App.git
git push -u origin main


# ─────────────────────────────────────────────────────────────
# STEP 8: BRANCH STRATEGY
# ─────────────────────────────────────────────────────────────
#
# Recommended branching model (simplified Git Flow):
#
#   main        →  Production-ready code only.
#                   Protected branch. Merges via Pull Request.
#
#   develop     →  Integration branch for features.
#                   All feature branches merge here first.
#
#   feature/*   →  Short-lived branches for new features.
#                   Example: feature/add-leaderboard
#
#   bugfix/*    →  Branches for bug fixes.
#                   Example: bugfix/fix-timer-reset
#
#   hotfix/*    →  Emergency fixes applied directly to main.
#                   Example: hotfix/patch-csrf-vulnerability
#
# ── Create the develop branch ───────────────────────────────

git checkout -b develop
git push -u origin develop

# ── Create a feature branch (example) ──────────────────────

git checkout -b feature/add-leaderboard develop

# ... make changes ...
git add .
git commit -m "feat(quiz): add leaderboard with top 10 scores"
git push -u origin feature/add-leaderboard

# Then open a Pull Request on GitHub:
#   feature/add-leaderboard → develop → main

# ── Switch back to main ────────────────────────────────────

git checkout main


# ─────────────────────────────────────────────────────────────
# STEP 9: RELEASE TAGGING
# ─────────────────────────────────────────────────────────────
#
# Semantic Versioning: MAJOR.MINOR.PATCH
#
#   MAJOR  →  Breaking changes (v2.0.0)
#   MINOR  →  New features, backward-compatible (v1.1.0)
#   PATCH  →  Bug fixes (v1.0.1)
#
# Tags mark specific commits as release points. GitHub can
# auto-generate release notes from tags.
#
# ── Tag the initial release ─────────────────────────────────

git tag -a v1.0.0 -m "v1.0.0 – Initial production release with Docker & CI/CD"
git push origin v1.0.0

# ── List all tags ───────────────────────────────────────────

git tag -l

# ── Create a GitHub Release (web UI) ───────────────────────
#
#   1. Go to your repo → "Releases" → "Create a new release"
#   2. Choose tag: v1.0.0
#   3. Title: v1.0.0 – Initial Release
#   4. Description: Paste the changelog or auto-generate notes
#   5. Click "Publish release"
#
# ── Future releases ────────────────────────────────────────

# After merging a new feature:
git tag -a v1.1.0 -m "v1.1.0 – Add leaderboard and quiz analytics"
git push origin v1.1.0


# ─────────────────────────────────────────────────────────────
# QUICK REFERENCE – COMPLETE WORKFLOW
# ─────────────────────────────────────────────────────────────
#
#   1. Clean up:      Remove __pycache__, venv, *.db, *.pyc
#   2. Init:          git init -b main
#   3. Configure:     git config user.name / user.email
#   4. Stage & commit (7 atomic commits by phase)
#   5. Create repo:   GitHub web UI or gh CLI
#   6. Push:          git remote add origin <url>
#                     git push -u origin main
#   7. Branch:        git checkout -b develop
#   8. Tag:           git tag -a v1.0.0 -m "Initial release"
#                     git push origin v1.0.0
