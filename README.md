# Dockerized Quiz Application Pipeline

A premium, production-ready interactive MCQ Quiz Application built with Flask, Bootstrap 5, and SQLite, fully containerized with Docker, and configured with a GitHub Actions CI/CD test and build validation pipeline.

---

## 🚀 Project Overview

This repository houses a full-stack, responsive quiz platform designed for both students and administrators. Users can take interactive quizzes with custom timers, review historical scores, and visualize their progress on interactive charts. Administrators gain access to a secure administrative suite to perform CRUD operations on quiz categories, manage question databases, view registered users, and inspect historical attempts log reports.

---

## ✨ Features

### 👤 User Features
- **Registration & Login**: Secure forms with password hashing (PBKDF2-SHA256), session state preservation, and next-page redirects.
- **Dynamic Dashboard**: View high-level statistics (total quizzes, averages, high scores), category summaries, and interactive canvas performance line charts.
- **Interactive Quiz Engine**: Delivers questions one-at-a-time, randomized ordering, countdown timers with visual alarms, and option state retention.
- **Result Evaluations**: Instant scoring calculations with comprehensive question audits mapping user inputs against correct keys.
- **Attempt History**: Log records detailing category completed dates, raw score ratios, and pass/fail indicators.

### 🔑 Admin Features
- **Administrative Suite**: Restricted path access containing links to all administrative settings.
- **Category CRUD**: Create and delete quiz categories.
- **Question Management**: Full control to add, edit, and delete questions with category filters and forms data recovery.
- **User Log**: Inspect registered user details, credentials, roles, and registration dates.
- **Scores Log**: Searchable logs showing user attempts, categories, raw scores, percentages, and completed dates.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.13, Flask, SQLAlchemy, Flask-Login, Flask-WTF (CSRF Protection)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript (Canvas API)
- **Database**: SQLite (persisted via Docker volumes)
- **DevOps**: Docker, Docker Compose, GitHub Actions CI/CD
- **Version Control**: Git

---

## 📁 Project Structure

```
Dockerized-Quiz-App/
├── app.py                          # Main Flask application entry point
├── config.py                       # Configuration settings (12-Factor App compliant)
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Multi-stage production Dockerfile
├── docker-compose.yml              # Local Docker Compose orchestrator
├── .env                            # Local environment configuration file
├── .dockerignore                   # Docker build ignore rules
├── .gitignore                      # Git tracking ignore rules
├── README.md                       # Documentation
├── models/
│   ├── __init__.py
│   └── models.py                   # ORM models (User, Category, Question, Attempt)
├── routes/
│   ├── __init__.py
│   ├── auth.py                     # Authentication routes (Login, Register)
│   ├── main.py                     # Dashboard routes
│   ├── quiz.py                     # Quiz taking engine routes
│   └── admin.py                    # Administrative CRUD routes
├── static/
│   ├── css/
│   │   └── style.css               # Design system, variables, custom radio styling
│   └── js/
│       └── main.js                 # Countdown timer, Canvas charts, alerts auto-dismissal
├── templates/
│   ├── base.html                   # Master base layout
│   ├── auth/                       # Login & Register views
│   ├── main/                       # User dashboard
│   ├── quiz/                       # Quiz delivery & history views
│   └── admin/                      # Administrative CRUD views
├── instance/                       # SQLite persistent directory
└── tests/
    ├── __init__.py
    └── test_app.py                 # Pytest/unittest suite configuration
```

---

## 📦 Getting Started

### 🐋 Run with Docker Compose (Recommended)

1. Ensure [Docker](https://www.docker.com/) is installed and running on your system.
2. Clone this repository and navigate to the directory:
   ```bash
   git clone <repository-url>
   cd Dockerized-Quiz-App
   ```
3. Boot up the service container:
   ```bash
   docker-compose up -d --build
   ```
4. Access the web interface at `http://localhost:5000`.
5. Access default seeded credentials:
   - **Regular User**: Register a new account via the UI.
   - **Admin User**: Log in with Email `admin@quizapp.com` and Password `Admin@123` (configured in `.env`).

### 🐍 Run Locally

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On MacOS/Linux:
   source venv/bin/activate
   ```
2. Install Python package dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python app.py
   ```
4. Access the development application at `http://localhost:5000`.

### 🧪 Run Tests

Execute the unit test suite locally:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📈 Future Improvements
- **Alternative Databases**: Migrating to PostgreSQL or MySQL for high-concurrency environments.
- **OAuth Integration**: Adding Google/GitHub social logins.
- **Detailed Analytics**: Enhanced graphical insights with sorting and export options for administrators.
