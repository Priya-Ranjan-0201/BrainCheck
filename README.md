# 🧠 BrainCheck

A minimal Flask quiz application built **exclusively** to demonstrate DevOps concepts: Docker containerization, CI/CD with GitHub Actions, and automated testing.

> **Note:** The application itself is intentionally simple. The focus is on deployment automation, not application features.

---

## 📋 Project Overview

BrainCheck is a 5-question multiple-choice quiz app. No login, no database, no admin panel — just a clean demonstration of:

- ✅ **Containerization** — Dockerfile & Docker Compose
- ✅ **CI/CD Pipeline** — GitHub Actions (test → build → verify)
- ✅ **Automated Testing** — pytest with 13 test cases
- ✅ **One-Command Deployment** — `docker compose up`

---

## 🎯 Objectives

| Objective | How It's Demonstrated |
|---|---|
| Automatic Deployment | `docker compose up` runs the entire app |
| Deployment Automation | Dockerfile + docker-compose.yml handle everything |
| CI/CD Pipeline | GitHub Actions runs tests and builds on every push |
| Automated Testing | pytest validates routes, scoring, and health checks |

---

## 🛠 Technology Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.13 | Runtime |
| Flask | 3.1.1 | Web framework |
| pytest | 8.3.5 | Testing |
| Docker | Latest | Containerization |
| Docker Compose | Latest | Orchestration |
| GitHub Actions | — | CI/CD |

---

## 📁 Folder Structure

```
BRAINCHECK/
├── app.py                    # Flask application (single file)
├── requirements.txt          # Python dependencies (2 packages)
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose config
├── .dockerignore             # Docker build exclusions
├── .gitignore                # Git exclusions
├── .env.example              # Environment variable template
├── README.md                 # This file
├── templates/
│   ├── home.html             # Landing page
│   ├── quiz.html             # Quiz page (5 MCQs)
│   └── result.html           # Score display
├── static/
│   └── style.css             # Stylesheet
├── tests/
│   └── test_app.py           # All automated tests
└── .github/workflows/
    └── ci.yml                # GitHub Actions pipeline
```

---

## 🚀 How to Run

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Priya-Ranjan-0201/BrainCheck.git
cd BrainCheck

# Run with Docker Compose (one command!)
docker compose up --build
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Stop the Application

```bash
docker compose down
```

---

## 🐳 Docker Commands

| Command | Description |
|---|---|
| `docker compose up --build` | Build and start the app |
| `docker compose up -d` | Start in background (detached) |
| `docker compose down` | Stop and remove containers |
| `docker compose logs` | View application logs |
| `docker compose ps` | Check container status |
| `docker build -t braincheck .` | Build image manually |
| `docker run -p 5000:5000 braincheck` | Run container manually |

---

## ⚙️ GitHub Actions

The CI/CD pipeline (`.github/workflows/ci.yml`) runs automatically on every push to `main`:

### Pipeline Flow

```
Push to main
    │
    ▼
┌─────────────┐     ┌──────────────────┐
│  Run Tests  │────▶│  Build Docker    │
│  (pytest)   │     │  Image & Verify  │
└─────────────┘     └──────────────────┘
```

### What It Does

1. **Checkout** — Clones the repository
2. **Setup Python 3.13** — Installs the runtime
3. **Install Dependencies** — `pip install -r requirements.txt`
4. **Run pytest** — Executes all 13 tests
5. **Build Docker Image** — `docker build -t braincheck:test .`
6. **Verify Container** — Starts the container and hits `/health`

---

## 🧪 Testing

### Run Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v
```

### Test Coverage

| Test | What It Verifies |
|---|---|
| `test_app_exists` | Flask app instance created |
| `test_app_is_testing` | Test mode enabled |
| `test_home_page_status` | Home page returns 200 |
| `test_home_page_content` | Home page has "BrainCheck" |
| `test_quiz_page_status` | Quiz page returns 200 |
| `test_quiz_page_has_questions` | All 5 questions rendered |
| `test_quiz_page_has_submit` | Submit button present |
| `test_result_all_correct` | 5/5 = 100% |
| `test_result_all_wrong` | 0/5 = 0% |
| `test_result_partial_score` | 3/5 = 60% |
| `test_result_no_answers` | Empty form = 0% |
| `test_health_check` | `/health` returns healthy |
| `test_questions_count` | Exactly 5 questions |
| `test_questions_have_required_fields` | Data integrity check |

---

## 🔮 Future Scope

This project can be extended to demonstrate additional DevOps concepts:

- **Multi-stage Docker builds** — Optimize image size
- **Docker volumes** — Persist data with SQLite
- **Environment-based configs** — Staging vs. production
- **Nginx reverse proxy** — Multi-container setup
- **Monitoring** — Prometheus + Grafana integration
- **Container registry** — Push images to Docker Hub / GHCR
- **Infrastructure as Code** — Terraform / Ansible integration
- **Kubernetes** — Orchestration with K8s manifests

---

## 📝 License

This project is for educational purposes.

---

<p align="center">Built with ❤️ to learn DevOps</p>
