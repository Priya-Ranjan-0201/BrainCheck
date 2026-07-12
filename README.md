# 🧠 BrainCheck

A simple, fully containerized MCQ quiz web application built with **Flask**, **Bootstrap 5**, and **SQLite**, deployed via **Docker**.

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://docker.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)](https://getbootstrap.com)

---

## What is BrainCheck?

BrainCheck is a quiz platform where students can register, pick a topic, and take a timed multiple-choice quiz. Admins can manage categories, questions, and users through a built-in control panel.

---

## Features

**Student side**
- Register and log in securely
- Pick from quiz categories (Python, JavaScript, Docker, General Knowledge)
- Take timed quizzes with instant results
- View attempt history and score trends on the dashboard

**Admin side**
- Add, edit, and delete quiz categories and questions
- View all registered users and their attempt history
- Seeded automatically on first run — no manual setup needed

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, Flask 3.x |
| ORM | Flask-SQLAlchemy (SQLite) |
| Auth | Flask-Login + Werkzeug hashing |
| CSRF | Flask-WTF |
| Frontend | Bootstrap 5.3 + Bootstrap Icons |
| Container | Docker (multi-stage build) |
| Orchestration | Docker Compose |

---

## Quick Start

### Option 1 — Docker Compose (recommended)

```bash
git clone https://github.com/Priya-Ranjan-0201/BrainCheck.git
cd BrainCheck
docker compose up -d --build
```

Open **http://localhost:5000** in your browser.

### Option 2 — Run locally without Docker

```bash
git clone https://github.com/Priya-Ranjan-0201/BrainCheck.git
cd BrainCheck

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
flask run
```

Open **http://127.0.0.1:5000**

---

## Default Login

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@braincheck.com` | `Admin@123` |
| Student | Register at `/auth/register` | — |

> Change the admin password via the `ADMIN_PASSWORD` environment variable before deploying.

---

## Project Structure

```
BrainCheck/
├── app.py                  # App factory + database seeding
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Compose orchestration
├── .env.example            # Environment variable template
│
├── models/
│   └── models.py           # SQLAlchemy models (User, Category, Question, Attempt)
│
├── routes/
│   ├── auth.py             # Login / register / logout
│   ├── main.py             # Dashboard
│   ├── quiz.py             # Quiz engine
│   └── admin.py            # Admin panel
│
├── templates/              # Jinja2 HTML templates
├── static/                 # CSS and JavaScript
└── tests/                  # Unit tests
```

---

## Environment Variables

Copy `.env.example` to `.env` and edit as needed:

```env
SECRET_KEY=your-secret-key-here
ADMIN_EMAIL=admin@braincheck.com
ADMIN_PASSWORD=Admin@123
QUIZ_TIME_LIMIT=300
DATABASE_URL=sqlite:///instance/database.db
```

---

## Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Docker Commands

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f web

# Stop
docker compose down

# Rebuild after code changes
docker compose up -d --build
```

---

## Screenshots

| Login | Dashboard | Quiz |
|-------|-----------|------|
| Simple login form | Score stats + history | Timed MCQ questions |

---

## License

This project was built as a Capstone Project for B.Tech CSE at **Lovely Professional University**.  
Feel free to use or fork it for learning purposes.

---

*Built by [Priya Ranjan](https://github.com/Priya-Ranjan-0201)*
