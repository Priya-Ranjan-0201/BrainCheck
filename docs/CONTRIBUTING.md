# 🤝 Contributing to BrainCheck

Thank you for your interest in contributing to **BrainCheck**! This guide outlines our development workflow, coding standards, testing expectations, and pull request procedures.

---

## 📑 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Environment Setup](#development-environment-setup)
- [Git Branching Strategy](#git-branching-strategy)
- [Code Style & Linting Guidelines](#code-style--linting-guidelines)
- [Testing Requirements](#testing-requirements)
- [Creating a Pull Request](#creating-a-pull-request)
- [Issue Reporting](#issue-reporting)

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for all contributors. Please treat fellow developers with respect, constructive feedback, and collaboration.

---

## Development Environment Setup

### Prerequisites:
- Python 3.13+
- Git
- Docker & Docker Compose (Optional for local mode, required for container testing)

### Step-by-Step Setup:

1. **Fork & Clone Repository**:
   ```bash
   git clone https://github.com/Priya-Ranjan-0201/BrainCheck.git
   cd BrainCheck
   ```

2. **Set up Python Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS / Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install flake8 pytest coverage
   ```

4. **Initialize Environment Variables**:
   ```bash
   cp .env.example .env
   ```

5. **Run Locally**:
   ```bash
   flask run --host=127.0.0.1 --port=5000
   ```

---

## Git Branching Strategy

We follow a structured branch naming convention:

- `feature/<feature-name>`: For new capabilities (e.g., `feature/leaderboard-ui`).
- `fix/<bug-description>`: For bug fixes (e.g., `fix/timer-auto-submit-null`).
- `docs/<doc-update>`: For documentation additions or revisions.
- `refactor/<target>`: For non-functional code improvements.

```bash
git checkout -b feature/dynamic-categories
```

---

## Code Style & Linting Guidelines

We adhere strictly to **PEP 8** standards with the following project-specific configurations:

- **Line Length**: Max 120 characters for docstrings and statements.
- **Imports**: Group imports in order:
  1. Standard library (`os`, `random`, `datetime`)
  2. Third-party packages (`flask`, `flask_login`, `werkzeug`)
  3. Internal application modules (`models.models`, `config`)
- **Linting Check**:
  ```bash
  # Check for critical errors
  flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

  # Run full style audit (relaxed to 120 characters)
  flake8 . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics
  ```

---

## Testing Requirements

All contributions that add new features or modify existing routes must include corresponding unit tests under `tests/test_app.py`.

### Running Tests:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Verification Checklist before Submitting PR:
- [ ] All unit tests pass with exit code `0`.
- [ ] No regression on default database seeding.
- [ ] CSRF protection and `@admin_required` decorators are applied to all sensitive routes.
- [ ] Docker build succeeds: `docker compose build`.

---

## Creating a Pull Request

1. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat(admin): add question filter by category"
   ```
2. **Push to your fork**:
   ```bash
   git push origin feature/my-new-feature
   ```
3. **Open a Pull Request**:
   - Provide a clear, descriptive PR title.
   - Describe the changes made and link any related issues.
   - Attach screenshots or terminal outputs where applicable.
   - Ensure the automated GitHub Actions CI check (`docker-ci.yml`) passes.

---

## Issue Reporting

When filing bug reports, please include:
- Operating System & Docker version.
- Python version.
- Steps to reproduce the unexpected behavior.
- Stack trace or console log excerpts.
