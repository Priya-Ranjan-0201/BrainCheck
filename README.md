# 🎓 Dockerized Quiz Application Pipeline

A **production-ready**, fully containerized, interactive MCQ (Multiple Choice Question) Quiz Application built with **Flask**, **Bootstrap 5**, and **SQLite**. The project includes a complete **Docker** containerization setup with a **GitHub Actions CI/CD** pipeline for automated testing and build validation.

> Built as a DevOps demonstration project showcasing the complete journey from local Flask development to production Docker deployment with continuous integration.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Live Demo Screenshots](#-live-demo-screenshots)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Run with Docker Compose](#-run-with-docker-compose-recommended)
  - [Run Locally](#-run-locally-without-docker)
- [Default Credentials](#-default-credentials)
- [Environment Variables](#-environment-variables)
- [Database Schema](#-database-schema)
- [API Routes Reference](#-api-routes-reference)
- [Testing](#-testing)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Docker Reference](#-docker-reference)
- [Deployment Checklist](#-deployment-checklist)
- [Troubleshooting](#-troubleshooting)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Project Overview

This repository houses a **full-stack, responsive quiz platform** designed for both students and administrators. The application follows the **12-Factor App** methodology, making it fully portable across development, staging, and production environments.

### What This Project Demonstrates

| Area | Implementation |
|------|---------------|
| **Backend Development** | Flask application factory pattern, Blueprint-based routing, SQLAlchemy ORM |
| **Frontend Development** | Bootstrap 5 responsive UI, Canvas API charts, countdown timers |
| **Authentication & Security** | Password hashing (PBKDF2-SHA256), session management, CSRF protection, role-based access |
| **Database Design** | Relational schema with foreign keys, cascading deletes, indexed queries |
| **Containerization** | Multi-stage Docker builds, non-root user, health checks, named volumes |
| **Orchestration** | Docker Compose with resource limits, log rotation, environment injection |
| **CI/CD** | GitHub Actions pipeline with lint → test → Docker build stages |
| **DevOps Best Practices** | `.gitignore`, `.dockerignore`, `.env` management, semantic versioning |

---

## ✨ Features

### 👤 User Features

| Feature | Description |
|---------|-------------|
| **Registration & Login** | Secure forms with PBKDF2-SHA256 password hashing, session state preservation, and next-page redirects |
| **Dynamic Dashboard** | High-level statistics (total quizzes taken, average scores, highest score), category summaries, and an interactive Canvas API performance line chart |
| **Interactive Quiz Engine** | Questions delivered one-at-a-time with randomized ordering, a countdown timer with visual alarm styling, and option state retention on navigation |
| **Result Evaluation** | Instant score calculation with a comprehensive question-by-question audit showing user answers mapped against correct keys |
| **Attempt History** | Full log of all past attempts showing category, date completed, raw score ratios, percentages, and pass/fail indicators |

### 🔑 Admin Features

| Feature | Description |
|---------|-------------|
| **Admin Dashboard** | Central hub with summary statistics (total users, categories, questions, attempts) and quick-navigation cards to all management views |
| **Category Management** | Create new quiz categories and delete existing ones (cascading deletion removes associated questions and attempts) |
| **Question Management** | Full CRUD — add, edit, and delete questions with category filters, pre-populated edit forms, and form data recovery on validation errors |
| **User Directory** | Inspect all registered users with details including full name, email, role, and registration date |
| **Scores & Attempts Log** | Searchable log of all quiz attempts across all users — displays user name, category, raw score, percentage, and completion date |
| **Role-Based Access Control** | Admin routes are protected with a decorator that verifies the `is_admin` property; unauthorized users are redirected |

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.13 | Core programming language |
| Flask | ≥ 3.0.0 | Web framework (application factory pattern) |
| Flask-SQLAlchemy | ≥ 3.1.1 | ORM for database operations |
| Flask-Login | ≥ 0.6.3 | User session and authentication management |
| Flask-WTF | ≥ 1.2.1 | Form processing and CSRF token protection |
| Werkzeug | ≥ 3.0.1 | PBKDF2-SHA256 password hashing utilities |
| python-dotenv | ≥ 1.0.0 | Environment variable loading from `.env` files |

### Frontend
| Technology | Purpose |
|-----------|---------|
| HTML5 | Semantic page structure |
| CSS3 | Custom styling with CSS variables and design tokens |
| JavaScript (ES6) | Countdown timer, Canvas API charts, alert auto-dismissal |
| Bootstrap 5 | Responsive grid layout, components, and utilities |

### Database
| Technology | Purpose |
|-----------|---------|
| SQLite | Lightweight relational database (persisted via Docker volumes) |

### DevOps
| Technology | Purpose |
|-----------|---------|
| Docker | Multi-stage image builds with non-root user and health checks |
| Docker Compose | Service orchestration with volumes, resource limits, and log rotation |
| GitHub Actions | CI/CD pipeline — lint, test, and Docker build validation |
| Git | Version control with conventional commits and semantic tags |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Browser (User)                      │
│                  http://localhost:5000                    │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTP
┌──────────────────────────▼──────────────────────────────┐
│                Docker Container (quizapp_web)             │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Flask Application (app.py)             │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │              Blueprints (routes/)             │  │  │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐ │  │  │
│  │  │  │ auth.py  │ │ main.py  │ │   quiz.py    │ │  │  │
│  │  │  │ Login    │ │Dashboard │ │ Quiz Engine  │ │  │  │
│  │  │  │ Register │ │ Stats    │ │ Results      │ │  │  │
│  │  │  └──────────┘ └──────────┘ └──────────────┘ │  │  │
│  │  │  ┌──────────────────────────────────────────┐│  │  │
│  │  │  │            admin.py                      ││  │  │
│  │  │  │  Categories · Questions · Users · Scores ││  │  │
│  │  │  └──────────────────────────────────────────┘│  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │                                                    │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │         SQLAlchemy ORM (models/)              │  │  │
│  │  │  User · QuizCategory · Question · QuizAttempt │  │  │
│  │  └──────────────────────┬───────────────────────┘  │  │
│  └─────────────────────────┼──────────────────────────┘  │
│                            │                              │
│  ┌─────────────────────────▼──────────────────────────┐  │
│  │          SQLite Database (instance/database.db)      │  │
│  └─────────────────────────────────────────────────────┘  │
│                   Mounted Volume: quiz_data               │
└──────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Dockerized-Quiz-App/
│
├── app.py                              # Application factory, extension init, database seeding
├── config.py                           # Configuration classes (Config, TestingConfig)
├── requirements.txt                    # Python package dependencies
│
├── models/
│   ├── __init__.py                     # Package initializer
│   └── models.py                       # ORM models: User, QuizCategory, Question, QuizAttempt
│
├── routes/
│   ├── __init__.py                     # Package initializer
│   ├── auth.py                         # Authentication: /auth/login, /auth/register, /auth/logout
│   ├── main.py                         # Dashboard: /dashboard/ (stats, charts)
│   ├── quiz.py                         # Quiz engine: /quiz/categories, /quiz/start, /quiz/result
│   └── admin.py                        # Admin CRUD: /admin/ (categories, questions, users, attempts)
│
├── templates/
│   ├── base.html                       # Master layout (navbar, footer, flash messages, CDN links)
│   ├── auth/
│   │   ├── login.html                  # Login form
│   │   └── register.html               # Registration form
│   ├── main/
│   │   └── dashboard.html              # User dashboard with stats cards and Canvas chart
│   ├── quiz/
│   │   ├── categories.html             # Category selection grid
│   │   ├── quiz.html                   # Quiz-taking interface with timer
│   │   ├── result.html                 # Score results with question-by-question review
│   │   └── attempts.html               # Quiz attempt history table
│   └── admin/
│       ├── dashboard.html              # Admin overview with summary statistics
│       ├── categories.html             # Category list with create/delete forms
│       ├── questions.html              # Question list with category filter
│       ├── add_question.html           # Add new question form
│       ├── edit_question.html          # Edit existing question form
│       ├── users.html                  # Registered users directory
│       └── attempts.html               # All attempts log (admin view)
│
├── static/
│   ├── css/
│   │   └── style.css                   # Design system: CSS variables, custom radio buttons, responsive utilities
│   └── js/
│       └── main.js                     # Countdown timer, Canvas performance charts, alert auto-dismiss
│
├── tests/
│   ├── __init__.py                     # Test package initializer
│   └── test_app.py                     # Unit tests: routing, auth, models, role protection, seeding
│
├── instance/                           # SQLite database directory (created at runtime, gitignored)
│
├── Dockerfile                          # Multi-stage production build (python:3.13-slim)
├── docker-compose.yml                  # Service orchestration with volumes, limits, health checks
├── .dockerignore                       # Optimized Docker build context exclusions
├── .gitignore                          # Git tracking exclusions
├── .env                                # Environment variables (gitignored – secrets)
├── .env.example                        # Safe environment template (committed)
│
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Base CI workflow
│       └── docker-ci.yml              # Full CI/CD: lint → test → Docker build & verify
│
├── DOCKER_COMMANDS.md                  # Docker CLI reference guide
├── DOCKER_COMPOSE_COMMANDS.md          # Docker Compose CLI reference guide
├── GITHUB_SETUP.md                     # Git init, commits, branches, and tags guide
├── DEPLOYMENT_CHECKLIST.md             # 50+ item production verification checklist
└── README.md                           # This file
```

---

## 📦 Getting Started

### Prerequisites

| Software | Minimum Version | Download |
|----------|----------------|----------|
| Docker Desktop | 24.0+ | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Git | 2.40+ | [git-scm.com](https://git-scm.com/downloads) |
| Python (for local dev only) | 3.13 | [python.org](https://www.python.org/downloads/) |

---

### 🐋 Run with Docker Compose (Recommended)

This is the fastest way to get the application running. Docker handles all dependencies automatically.

**1. Clone the repository:**
```bash
git clone https://github.com/<your-username>/Dockerized-Quiz-App.git
cd Dockerized-Quiz-App
```

**2. Configure environment variables:**
```bash
# Copy the template and customize values
cp .env.example .env

# Generate a strong secret key
python -c "import secrets; print(secrets.token_hex(32))"
# Paste the output into SECRET_KEY in .env
```

**3. Build and start the container:**
```bash
docker compose up -d --build
```

**4. Verify the container is healthy:**
```bash
docker compose ps
# STATUS should show "Up" and "(healthy)"
```

**5. Open the application:**
```
http://localhost:5000
```

**6. Stop the application:**
```bash
docker compose down          # Stops container (keeps database)
docker compose down -v       # Stops AND deletes database volume
```

---

### 🐍 Run Locally (Without Docker)

**1. Create and activate a virtual environment:**
```bash
# Create
python -m venv venv

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activate (macOS / Linux)
source venv/bin/activate
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure environment (optional):**
```bash
cp .env.example .env
# Edit .env with your preferred values
```

**4. Run the development server:**
```bash
python app.py
```

**5. Open the application:**
```
http://localhost:5000
```

The database and seed data (admin user, categories, sample questions) are created automatically on first run.

---

## 🔐 Default Credentials

| Role | Email | Password | Notes |
|------|-------|----------|-------|
| **Admin** | `admin@quizapp.com` | `Admin@123` | Full access to admin panel |
| **User** | — | — | Register via the UI at `/auth/register` |

> ⚠️ **Change the admin password** before deploying to production! Update `ADMIN_PASSWORD` in your `.env` file.

---

## ⚙️ Environment Variables

All configuration is managed through environment variables, loaded from the `.env` file. The application provides sensible defaults for every variable.

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_APP` | `app.py` | Flask application entry point |
| `FLASK_ENV` | `production` | Environment mode (`production` or `development`) |
| `FLASK_HOST` | `0.0.0.0` | Server bind address |
| `FLASK_PORT` | `5000` | Server port number |
| `FLASK_DEBUG` | `False` | Enable/disable debug mode and auto-reloader |
| `PORT` | `5000` | Docker-level port (used by EXPOSE and Compose) |
| `SECRET_KEY` | *(weak default)* | Signs sessions and CSRF tokens — **must change in production** |
| `DATABASE_URL` | `sqlite:///instance/database.db` | SQLAlchemy database connection string |
| `SESSION_COOKIE_SECURE` | `False` | Set `True` when serving over HTTPS |
| `SESSION_COOKIE_HTTPONLY` | `True` | Prevents JavaScript access to session cookies |
| `SESSION_COOKIE_SAMESITE` | `Lax` | Cross-site request restriction level |
| `ADMIN_EMAIL` | `admin@quizapp.com` | Seed admin account email |
| `ADMIN_PASSWORD` | `Admin@123` | Seed admin account password — **change in production** |
| `QUIZ_TIME_LIMIT` | `300` | Quiz countdown timer in seconds (5 minutes) |

**Generate a secure `SECRET_KEY`:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🗄️ Database Schema

The application uses four SQLAlchemy models stored in an SQLite database:

```
┌──────────────────┐       ┌────────────────────┐
│      users       │       │  quiz_categories   │
├──────────────────┤       ├────────────────────┤
│ id (PK)          │       │ id (PK)            │
│ fullname         │       │ name (UNIQUE)      │
│ email (UNIQUE)   │       └────────┬───────────┘
│ password_hash    │                │
│ role             │       ┌────────▼───────────┐
│ created_at       │       │    questions       │
└────────┬─────────┘       ├────────────────────┤
         │                 │ id (PK)            │
         │                 │ category_id (FK)   │
         │                 │ question           │
         │                 │ option_a/b/c/d     │
         │                 │ correct_option     │
         │                 └────────────────────┘
         │
┌────────▼──────────────────────────┐
│          quiz_attempts            │
├───────────────────────────────────┤
│ id (PK)                           │
│ user_id (FK → users.id)          │
│ category_id (FK → quiz_categories)│
│ score                             │
│ total_questions                   │
│ percentage                        │
│ completed_at                      │
└───────────────────────────────────┘
```

**Key relationships:**
- A **User** has many **QuizAttempts** (one-to-many, cascade delete)
- A **QuizCategory** has many **Questions** (one-to-many, cascade delete)
- A **QuizCategory** has many **QuizAttempts** (one-to-many, cascade delete)

---

## 🌐 API Routes Reference

### Authentication (`/auth`)

| Method | Route | Auth Required | Description |
|--------|-------|:------------:|-------------|
| GET/POST | `/auth/login` | ❌ | Login form and handler |
| GET/POST | `/auth/register` | ❌ | Registration form and handler |
| GET | `/auth/logout` | ✅ | Ends session, redirects to login |

### Dashboard (`/`)

| Method | Route | Auth Required | Description |
|--------|-------|:------------:|-------------|
| GET | `/` | ✅ | Redirects to `/dashboard/` |
| GET | `/dashboard/` | ✅ | User dashboard with stats and chart |

### Quiz Engine (`/quiz`)

| Method | Route | Auth Required | Description |
|--------|-------|:------------:|-------------|
| GET | `/quiz/categories` | ✅ | List available quiz categories |
| GET/POST | `/quiz/start/<id>` | ✅ | Start quiz and submit answers |
| GET | `/quiz/result/<id>` | ✅ | View quiz results with answer review |
| GET | `/quiz/attempts` | ✅ | View personal attempt history |

### Admin Panel (`/admin`)

| Method | Route | Auth Required | Admin Only | Description |
|--------|-------|:------------:|:---------:|-------------|
| GET | `/admin/` | ✅ | ✅ | Admin dashboard overview |
| GET/POST | `/admin/categories` | ✅ | ✅ | Manage categories (create/delete) |
| GET | `/admin/questions` | ✅ | ✅ | List questions with filters |
| GET/POST | `/admin/questions/add` | ✅ | ✅ | Add a new question |
| GET/POST | `/admin/questions/edit/<id>` | ✅ | ✅ | Edit an existing question |
| POST | `/admin/questions/delete/<id>` | ✅ | ✅ | Delete a question |
| GET | `/admin/users` | ✅ | ✅ | View registered users |
| GET | `/admin/attempts` | ✅ | ✅ | View all quiz attempts |

---

## 🧪 Testing

The project includes a unit test suite in `tests/test_app.py` that covers:

| Test | What It Verifies |
|------|-----------------|
| `test_index_redirects_to_dashboard` | Root URL (`/`) returns a 302 redirect to the dashboard |
| `test_dashboard_unauthenticated_redirect` | Unauthenticated access to `/dashboard/` redirects to login |
| `test_user_registration` | Valid registration creates a user in the database |
| `test_user_login_validation` | Invalid login credentials show an error message |
| `test_admin_route_protection_by_default` | Regular users cannot access admin routes |
| `test_database_category_seed` | Default categories and questions are seeded on startup |

**Run tests locally:**
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

**Run tests in Docker:**
```bash
docker compose run --rm web python -m unittest discover -s tests -p "test_*.py" -v
```

Tests use an **in-memory SQLite database** via `TestingConfig` — no data files are created or modified.

---

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/docker-ci.yml`) that automatically runs on every push and pull request to the `main` and `develop` branches.

### Pipeline Stages

```
Push / Pull Request
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│  🔍 Lint     │ ──▶ │  🧪 Test     │ ──▶ │  🐳 Docker Build │
│  (flake8)   │     │  (unittest) │     │  (build + curl)  │
└─────────────┘     └─────────────┘     └──────────────────┘
```

| Stage | Tool | What It Checks | Blocks Merge? |
|-------|------|---------------|:-------------:|
| **Lint** | flake8 | Python syntax errors, undefined names | ✅ (critical only) |
| **Test** | unittest | All 6 test cases pass | ✅ |
| **Docker Build** | Docker + curl | Image builds, container starts, HTTP 200/302 response | ✅ |

### Additional Features
- **Concurrency control** — cancels in-progress runs when new commits are pushed
- **Docker Buildx** — modern build engine with improved layer caching
- **Dual image tagging** — `:latest` and `:git-sha` for traceability
- **Always-on log capture** — container logs are printed even on failure

---

## 🐳 Docker Reference

### Image Details

| Property | Value |
|----------|-------|
| Base image | `python:3.13-slim` (~50 MB) |
| Build type | Multi-stage (builder → final) |
| Runtime user | `appuser` (non-root) |
| Exposed port | `5000` |
| Health check | HTTP ping every 30s with 3 retries |

### Quick Commands

```bash
# Build and start
docker compose up -d --build

# View status
docker compose ps

# Follow logs
docker compose logs -f web

# Restart
docker compose restart web

# Stop (keep data)
docker compose down

# Stop and DELETE data
docker compose down -v

# Shell into container
docker compose exec web /bin/bash

# Check who the container runs as
docker exec quizapp_web whoami
# → appuser
```

For detailed command references, see:
- [`DOCKER_COMMANDS.md`](DOCKER_COMMANDS.md) — Docker CLI guide
- [`DOCKER_COMPOSE_COMMANDS.md`](DOCKER_COMPOSE_COMMANDS.md) — Docker Compose CLI guide

---

## ✅ Deployment Checklist

Before declaring the application production-ready, verify:

- [ ] Docker image builds without errors (`docker compose build`)
- [ ] Container starts and shows "healthy" status
- [ ] Website opens at `http://localhost:5000`
- [ ] Admin login works with seeded credentials
- [ ] User registration and login flow works
- [ ] Quiz selection → taking → results → history works end-to-end
- [ ] Database persists across `docker compose restart`
- [ ] Database persists across `docker compose down && docker compose up -d`
- [ ] Admin CRUD operations work (categories, questions)
- [ ] `SECRET_KEY` is a strong random value
- [ ] `ADMIN_PASSWORD` has been changed
- [ ] `FLASK_DEBUG` is set to `False`
- [ ] `.env` is NOT committed to Git
- [ ] GitHub Actions CI/CD pipeline passes all 3 stages

For the full 50+ item checklist, see [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md).

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Container exits immediately** | Check logs: `docker compose logs web` — look for Python tracebacks |
| **Port 5000 already in use** | Change `PORT` in `.env` to another value (e.g., `8080`) and update the port mapping |
| **Database is empty after restart** | Verify the named volume: `docker volume ls \| grep quizapp`. If missing, the volume wasn't mounted correctly |
| **CSS/JS not loading** | Check browser DevTools → Network tab for 404s. Ensure `static/` folder is included in the Docker image |
| **CSRF token missing** | Ensure `flask-wtf` is installed and `CSRFProtect` is initialized in `app.py` |
| **Permission denied in container** | The `instance/` directory must be owned by `appuser`. Rebuild the image: `docker compose build --no-cache` |
| **Git says "nothing to commit"** | All files are already committed. Check `git status` and `git log --oneline` |
| **GitHub Actions failing** | Click the failed job in the Actions tab → read the error log. Common causes: flake8 syntax errors, failed tests |

---

## 📈 Future Improvements

- **Production WSGI Server** — Replace Flask dev server with Gunicorn for production concurrency
- **PostgreSQL/MySQL** — Migrate from SQLite for high-concurrency environments
- **OAuth Integration** — Add Google/GitHub social login options
- **Leaderboard System** — Global and per-category leaderboards with top scores
- **Question Import/Export** — CSV/JSON bulk upload for quiz content management
- **Detailed Analytics** — Enhanced graphical insights with sorting, filtering, and export for administrators
- **Email Notifications** — Password reset and quiz completion notifications
- **Rate Limiting** — Protect login and registration endpoints from brute force attacks

---

## 🤝 Contributing

1. **Fork** this repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m "feat: add your feature description"`
4. **Push** to your fork: `git push origin feature/your-feature-name`
5. **Open** a Pull Request against the `develop` branch

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) format for commit messages.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ by PRIYE RANJAN**

Python · Flask · Docker · GitHub Actions

</div>
