# ============================================================
# GitHub Repository Preparation Guide
# Dockerized Quiz Application
# ============================================================
#
# This guide covers the complete journey from a local project
# to a professional GitHub repository: cleanup, Git init,
# commit strategy, branching model, and release tagging.
#
# Prerequisites:
#   • Git installed → https://git-scm.com/downloads
#   • GitHub account → https://github.com
#   • Terminal open in the project root (Dockerized-Quiz-App/)
# ============================================================


# ─────────────────────────────────────────────────────────────
# STEP 1: INSTALL & CONFIGURE GIT
# ─────────────────────────────────────────────────────────────
#
# If Git is already installed, skip to Step 2.
#
# Download: https://git-scm.com/downloads
#
# During Windows installation:
#   • Default editor: Choose VS Code or your preferred editor
#   • PATH: Select "Git from the command line and also from
#            3rd-party software"
#   • Line endings: "Checkout Windows-style, commit Unix-style"
#   • Everything else: Use defaults
#
# Verify installation:

git --version
# Expected: git version 2.x.x

# Configure your identity (used in every commit):
git config --global user.name "PRIYE RANJAN"
git config --global user.email "your-email@example.com"

# Verify configuration:
git config --list --show-origin

# Optional but recommended settings:
git config --global init.defaultBranch main        # Use "main" instead of "master"
git config --global core.autocrlf true             # Handle Windows line endings
git config --global pull.rebase false              # Merge on pull (safe default)


# ─────────────────────────────────────────────────────────────
# STEP 2: FOLDER CLEANUP
# ─────────────────────────────────────────────────────────────
#
# Before making your first commit, remove generated files that
# should NOT be in the repository. While .gitignore prevents
# them from being TRACKED, existing files in the working
# directory must be deleted manually first.
#
# Why this matters:
#   • __pycache__/ and *.pyc are Python bytecode — not portable
#   • venv/ is hundreds of MB — each contributor creates their own
#   • instance/*.db contains local data — recreated on startup
#   • .env contains secrets — NEVER commit credentials
#
# ── Cleanup Commands (PowerShell) ────────────────────────────

# Remove all __pycache__ directories recursively:
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Remove virtual environment directories:
if (Test-Path ".venv") { Remove-Item -Recurse -Force ".venv" }
if (Test-Path "venv")  { Remove-Item -Recurse -Force "venv"  }

# Remove compiled Python bytecode files:
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
Get-ChildItem -Recurse -Filter "*.pyo" | Remove-Item -Force

# Remove SQLite database files from instance/:
if (Test-Path "instance") {
    Get-ChildItem "instance" -Filter "*.db" | Remove-Item -Force
}

# Remove pytest cache:
if (Test-Path ".pytest_cache") { Remove-Item -Recurse -Force ".pytest_cache" }

# Remove IDE configuration directories:
if (Test-Path ".vscode") { Remove-Item -Recurse -Force ".vscode" }
if (Test-Path ".idea")   { Remove-Item -Recurse -Force ".idea" }

# ── Cleanup Commands (macOS / Linux Bash) ────────────────────

# find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
# find . -name "*.pyc" -delete
# rm -rf .venv venv .pytest_cache .vscode .idea
# rm -f instance/*.db


# ─────────────────────────────────────────────────────────────
# STEP 3: VERIFY PROJECT STRUCTURE
# ─────────────────────────────────────────────────────────────
#
# After cleanup, your project tree should look exactly like
# this. Files marked with (gitignored) will NOT be committed.
#
# Dockerized-Quiz-App/
# ├── .dockerignore                    ← Committed
# ├── .env                             ← (gitignored) secrets
# ├── .env.example                     ← Committed (safe template)
# ├── .github/
# │   └── workflows/
# │       ├── ci.yml                   ← Committed
# │       └── docker-ci.yml           ← Committed
# ├── .gitignore                       ← Committed
# ├── Dockerfile                       ← Committed
# ├── DEPLOYMENT_CHECKLIST.md          ← Committed
# ├── DOCKER_COMMANDS.md               ← Committed
# ├── DOCKER_COMPOSE_COMMANDS.md       ← Committed
# ├── GITHUB_SETUP.md                  ← Committed
# ├── README.md                        ← Committed
# ├── app.py                           ← Committed
# ├── config.py                        ← Committed
# ├── docker-compose.yml               ← Committed
# ├── instance/                        ← (gitignored) runtime DB
# ├── models/
# │   ├── __init__.py                  ← Committed
# │   └── models.py                    ← Committed
# ├── requirements.txt                 ← Committed
# ├── routes/
# │   ├── __init__.py                  ← Committed
# │   ├── admin.py                     ← Committed
# │   ├── auth.py                      ← Committed
# │   ├── main.py                      ← Committed
# │   └── quiz.py                      ← Committed
# ├── static/
# │   ├── css/style.css                ← Committed
# │   └── js/main.js                   ← Committed
# ├── templates/ (all .html files)     ← Committed
# └── tests/
#     ├── __init__.py                  ← Committed
#     └── test_app.py                  ← Committed
#
# Verify with this command (PowerShell):
Get-ChildItem -Recurse -File | Where-Object {
    $_.FullName -notmatch '\\(\.venv|venv|__pycache__|\.git|instance)\\' -and
    $_.Name -notmatch '\.(pyc|db|sqlite3)$'
} | Select-Object FullName


# ─────────────────────────────────────────────────────────────
# STEP 4: INITIALIZE THE GIT REPOSITORY
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Creates a hidden .git/ directory that contains all version
#   control data — the commit history, branches, tags, and
#   configuration.
#
# The -b flag sets the default branch name to "main"
# (the modern industry standard, replacing the legacy "master").
#
# ⚠️ Only run this once. If .git/ already exists, skip this.

git init -b main


# ─────────────────────────────────────────────────────────────
# STEP 5: COMMIT STRATEGY
# ─────────────────────────────────────────────────────────────
#
# Why structured commits matter:
#   • Each commit is a logical, reviewable unit of work
#   • git log tells a clear story of how the project was built
#   • git bisect can isolate exactly which commit introduced a bug
#   • Pull requests are easier to review
#   • Automated changelogs can be generated from commit messages
#
# Commit message format (Conventional Commits standard):
#
#   <type>(<scope>): <short description>
#
#   Types and when to use them:
#   ┌──────────┬────────────────────────────────────────────┐
#   │ Type     │ When to use                                │
#   ├──────────┼────────────────────────────────────────────┤
#   │ feat     │ A new feature or capability                │
#   │ fix      │ A bug fix                                  │
#   │ docs     │ Documentation only (README, comments)      │
#   │ style    │ Formatting changes (no logic change)       │
#   │ refactor │ Code restructuring (no new feature or fix) │
#   │ test     │ Adding or updating tests                   │
#   │ ci       │ CI/CD pipeline changes                     │
#   │ chore    │ Build tools, config, dependencies          │
#   └──────────┴────────────────────────────────────────────┘
#
# ─────────────────────────────────────────────────────────────

# ── Commit 1: Core Application ──────────────────────────────
# What: Flask app factory, config, models, routes, dependencies
# Why first: Everything else depends on the backend

git add app.py config.py requirements.txt
git add models/ routes/
git commit -m "feat(app): add Flask application with auth, quiz engine, and admin panel"

# ── Commit 2: Frontend ──────────────────────────────────────
# What: All HTML templates, CSS design system, JavaScript
# Why separate: Frontend can be reviewed independently

git add templates/ static/
git commit -m "feat(ui): add Bootstrap 5 templates and interactive JS components"

# ── Commit 3: Tests ─────────────────────────────────────────
# What: Unit test suite and test configuration
# Why separate: Tests validate the app but are not the app

git add tests/
git commit -m "test(app): add unit test suite for core application features"

# ── Commit 4: Docker Configuration ──────────────────────────
# What: Dockerfile, docker-compose.yml, .dockerignore
# Why separate: Docker is an infrastructure concern

git add Dockerfile docker-compose.yml .dockerignore
git commit -m "chore(docker): add multi-stage Dockerfile and Compose orchestration"

# ── Commit 5: Environment & Git Config ──────────────────────
# What: .gitignore and .env.example (NOT .env itself!)
# Why separate: Configuration management is its own concern

git add .gitignore .env.example
git commit -m "chore(config): add .gitignore and .env.example template"

# ── Commit 6: Documentation ─────────────────────────────────
# What: README and all guide files
# Why separate: Docs don't affect code behavior

git add README.md DOCKER_COMMANDS.md DOCKER_COMPOSE_COMMANDS.md
git add DEPLOYMENT_CHECKLIST.md GITHUB_SETUP.md
git commit -m "docs: add README, Docker guides, GitHub setup, and deployment checklist"

# ── Commit 7: CI/CD Pipeline ────────────────────────────────
# What: GitHub Actions workflow files
# Why last: CI validates everything above

git add .github/
git commit -m "ci(github-actions): add Docker build and test validation pipeline"

# ── Verify commit history ───────────────────────────────────
git log --oneline --decorate
# Expected output (newest first):
#   abc1234 (HEAD -> main) ci(github-actions): add Docker build and test validation pipeline
#   def5678 docs: add README, Docker guides, GitHub setup, and deployment checklist
#   ghi9012 chore(config): add .gitignore and .env.example template
#   jkl3456 chore(docker): add multi-stage Dockerfile and Compose orchestration
#   mno7890 test(app): add unit test suite for core application features
#   pqr1234 feat(ui): add Bootstrap 5 templates and interactive JS components
#   stu5678 feat(app): add Flask application with auth, quiz engine, and admin panel

# Verify nothing is left uncommitted:
git status
# Expected: "nothing to commit, working tree clean"

# Verify .env is NOT tracked:
git ls-files .env
# Expected: (no output — .env is properly ignored)


# ─────────────────────────────────────────────────────────────
# STEP 6: CREATE THE GITHUB REPOSITORY
# ─────────────────────────────────────────────────────────────
#
# ── Option A: GitHub Web UI (Recommended for beginners) ──────
#
#   1. Go to https://github.com/new
#
#   2. Fill in the form:
#      • Repository name:  Dockerized-Quiz-App
#      • Description:      Production-ready Flask Quiz Application
#                           with Docker & CI/CD pipeline
#      • Visibility:       Public (or Private if preferred)
#
#   3. ⚠️ IMPORTANT — Do NOT check any of these boxes:
#      ☐ Add a README file
#      ☐ Add .gitignore
#      ☐ Choose a license
#
#      Why: We already have all of these locally. If GitHub
#      creates them, you'll get a merge conflict on your first
#      push because both local and remote have different initial
#      commits.
#
#   4. Click "Create repository"
#
#   5. GitHub will show you the "push an existing repository"
#      commands — use them in Step 7 below.
#
# ── Option B: GitHub CLI (Faster, if gh is installed) ────────
#
#   Install: https://cli.github.com/
#
#   gh auth login                          # Authenticate once
#   gh repo create Dockerized-Quiz-App \
#     --public \
#     --source=. \
#     --remote=origin \
#     --description "Production-ready Flask Quiz Application with Docker & CI/CD"


# ─────────────────────────────────────────────────────────────
# STEP 7: CONNECT & PUSH TO GITHUB
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Links your local repository to the remote GitHub repo
#   and uploads all commits.
#
# "origin" is the conventional name for your primary remote.
# "-u" sets the upstream tracking, so future pushes only
# need "git push" (no arguments).
#
# ⚠️ Replace <your-username> with your actual GitHub username.

# Add the remote repository:
git remote add origin https://github.com/<your-username>/Dockerized-Quiz-App.git

# Push all commits to GitHub:
git push -u origin main

# Verify the remote is configured:
git remote -v
# Expected:
#   origin  https://github.com/<your-username>/Dockerized-Quiz-App.git (fetch)
#   origin  https://github.com/<your-username>/Dockerized-Quiz-App.git (push)

# ── Authentication ──────────────────────────────────────────
#
# Git will ask for credentials on the first push.
#
# Option 1: Personal Access Token (PAT)
#   1. Go to: GitHub → Settings → Developer Settings →
#             Personal Access Tokens → Tokens (classic)
#   2. Generate a new token with "repo" scope
#   3. Use it as the password when Git prompts
#
# Option 2: GitHub CLI
#   gh auth login
#   (handles authentication automatically)
#
# Option 3: SSH Key
#   ssh-keygen -t ed25519 -C "your-email@example.com"
#   # Add the public key to GitHub → Settings → SSH Keys
#   git remote set-url origin git@github.com:<your-username>/Dockerized-Quiz-App.git


# ─────────────────────────────────────────────────────────────
# STEP 8: BRANCH STRATEGY
# ─────────────────────────────────────────────────────────────
#
# A branching model ensures code quality and prevents broken
# code from reaching production. This project uses a
# simplified Git Flow model:
#
# Branch hierarchy:
#
#   main
#    │  ← Production-ready code only
#    │  ← Merges via reviewed Pull Requests
#    │  ← Tagged with version numbers (v1.0.0)
#    │  ← Protected branch (no direct pushes)
#    │
#    ├── develop
#    │    │  ← Integration branch
#    │    │  ← All features merge here first
#    │    │  ← Periodically merged to main via PR
#    │    │
#    │    ├── feature/add-leaderboard
#    │    │     ← Short-lived feature branches
#    │    │     ← Created from develop
#    │    │     ← Merged back to develop via PR
#    │    │
#    │    └── feature/add-analytics
#    │
#    ├── bugfix/fix-timer-reset
#    │     ← Non-critical bug fixes
#    │     ← Branch from develop, merge to develop
#    │
#    └── hotfix/patch-csrf-vulnerability
#          ← Emergency fixes for production
#          ← Branch from main, merge to main AND develop
#
# ── Branch naming conventions ───────────────────────────────
#
#   feature/<descriptive-name>    →  New features
#   bugfix/<descriptive-name>     →  Non-urgent bug fixes
#   hotfix/<descriptive-name>     →  Critical production fixes
#   docs/<descriptive-name>       →  Documentation updates
#   refactor/<descriptive-name>   →  Code restructuring
#
# ── Create the develop branch ───────────────────────────────

git checkout -b develop
git push -u origin develop

# ── Feature branch workflow (example) ───────────────────────

# 1. Create a feature branch from develop:
git checkout develop
git checkout -b feature/add-leaderboard

# 2. Make your changes and commit:
git add .
git commit -m "feat(quiz): add leaderboard with top 10 scores"

# 3. Push the feature branch to GitHub:
git push -u origin feature/add-leaderboard

# 4. Open a Pull Request on GitHub:
#    feature/add-leaderboard → develop
#    (request code review from teammates)

# 5. After the PR is approved and merged, clean up:
git checkout develop
git pull origin develop
git branch -d feature/add-leaderboard
git push origin --delete feature/add-leaderboard

# ── Switch back to main ────────────────────────────────────

git checkout main

# ── Protecting branches on GitHub ───────────────────────────
#
# Go to: Repository → Settings → Branches → Branch protection rules
#
# For "main":
#   ✅ Require a pull request before merging
#   ✅ Require status checks to pass before merging
#      → Select "CI/CD Quiz App Pipeline"
#   ✅ Require branches to be up to date before merging
#   ❌ Allow force pushes (keep disabled)
#   ❌ Allow deletions (keep disabled)


# ─────────────────────────────────────────────────────────────
# STEP 9: RELEASE TAGGING
# ─────────────────────────────────────────────────────────────
#
# Tags mark specific commits as release points. They appear
# on GitHub under "Releases" and can trigger deployment
# workflows.
#
# Format: Semantic Versioning (SemVer)
#
#   v MAJOR . MINOR . PATCH
#
#   MAJOR  →  Breaking changes that require user action
#             (v1.0.0 → v2.0.0)
#   MINOR  →  New features, fully backward-compatible
#             (v1.0.0 → v1.1.0)
#   PATCH  →  Bug fixes, no new features
#             (v1.0.0 → v1.0.1)
#
# Examples:
#   v1.0.0  →  Initial production release
#   v1.1.0  →  Added leaderboard feature
#   v1.1.1  →  Fixed timer display bug
#   v2.0.0  →  Migrated from SQLite to PostgreSQL (breaking)
#
# ── Tag the initial release ─────────────────────────────────

# Create an annotated tag (includes author, date, message):
git tag -a v1.0.0 -m "v1.0.0 - Initial production release with Docker and CI/CD pipeline"

# Push the tag to GitHub:
git push origin v1.0.0

# ── List all tags ───────────────────────────────────────────

git tag -l

# Show tag details:
git show v1.0.0

# ── Create a GitHub Release (web UI) ───────────────────────
#
#   1. Go to your repo → "Releases" tab → "Create a new release"
#   2. Choose tag: v1.0.0
#   3. Title: v1.0.0 — Initial Production Release
#   4. Description: Summarize what's included:
#
#      ## What's Included
#      - Flask quiz application with user and admin roles
#      - Interactive quiz engine with countdown timers
#      - Admin panel with full CRUD operations
#      - Docker containerization (multi-stage build)
#      - Docker Compose orchestration with volumes
#      - GitHub Actions CI/CD pipeline
#      - Comprehensive documentation
#
#   5. Click "Publish release"

# ── Future releases ────────────────────────────────────────

# After merging a feature from develop to main:
git checkout main
git pull origin main
git tag -a v1.1.0 -m "v1.1.0 - Add leaderboard and quiz analytics"
git push origin v1.1.0

# After a bug fix:
git tag -a v1.1.1 -m "v1.1.1 - Fix timer not resetting between quizzes"
git push origin v1.1.1

# Delete a tag (if you made a mistake):
git tag -d v1.1.1                    # Delete locally
git push origin --delete v1.1.1      # Delete from GitHub


# ─────────────────────────────────────────────────────────────
# STEP 10: POST-PUSH VERIFICATION
# ─────────────────────────────────────────────────────────────
#
# After pushing to GitHub, verify everything is correct:
#
# ── On GitHub ───────────────────────────────────────────────
#
#   1. Repository page:
#      [ ] README.md renders correctly with formatting
#      [ ] Project structure matches local
#      [ ] .env is NOT visible (properly gitignored)
#      [ ] .env.example IS visible
#
#   2. Actions tab:
#      [ ] CI/CD workflow triggered automatically
#      [ ] All 3 stages pass (Lint → Test → Docker Build)
#
#   3. Releases tab:
#      [ ] v1.0.0 tag appears
#      [ ] Release notes are present
#
# ── Locally ─────────────────────────────────────────────────

git status
# → "nothing to commit, working tree clean"

git log --oneline -n 7
# → Shows all 7 commits

git remote -v
# → Shows the GitHub URL

git tag -l
# → Shows v1.0.0


# ─────────────────────────────────────────────────────────────
# QUICK REFERENCE — COMPLETE WORKFLOW
# ─────────────────────────────────────────────────────────────
#
#   1. Install Git          → git --version
#   2. Configure identity   → git config user.name / user.email
#   3. Clean up project     → Remove __pycache__, venv, *.db
#   4. Initialize repo      → git init -b main
#   5. Commit (7 commits)   → Staged by logical component
#   6. Create GitHub repo   → github.com/new (no init files!)
#   7. Add remote + push    → git remote add origin <url>
#                             git push -u origin main
#   8. Create develop       → git checkout -b develop
#                             git push -u origin develop
#   9. Tag release          → git tag -a v1.0.0 -m "..."
#                             git push origin v1.0.0
#  10. Verify on GitHub     → README, Actions, Releases tabs
