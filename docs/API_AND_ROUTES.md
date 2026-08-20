# 🚦 BrainCheck API & Route Reference

This document provides a complete reference for all routes, blueprints, HTTP methods, authorization levels, parameters, and behaviors in the **BrainCheck** web application.

---

## 📑 Table of Contents

- [Overview & Route Conventions](#overview--route-conventions)
- [Root Routing](#root-routing)
- [Authentication Blueprint (`auth_bp`)](#authentication-blueprint-auth_bp)
- [Dashboard Blueprint (`main_bp`)](#dashboard-blueprint-main_bp)
- [Quiz Engine Blueprint (`quiz_bp`)](#quiz-engine-blueprint-quiz_bp)
- [Admin Blueprint (`admin_bp`)](#admin-blueprint-admin_bp)
- [Error Handling & Redirect Semantics](#error-handling--redirect-semantics)

---

## Overview & Route Conventions

- **Session Authentication**: Protected endpoints require standard session cookie generated upon successful login.
- **CSRF Tokens**: All `POST` endpoints must submit a valid `csrf_token` in form data.
- **URL Prefixes**:
  - Auth: `/auth`
  - Main/Dashboard: `/dashboard`
  - Quiz Engine: `/quiz`
  - Admin Portal: `/admin`

---

## Root Routing

### `GET /`
- **Controller**: `app.index`
- **Access Level**: Public
- **Behavior**: Redirects immediately to `main.dashboard` (`/dashboard/`).
- **Response**: `302 Found` -> `Location: /dashboard/`

---

## Authentication Blueprint (`auth_bp`)

### `GET /auth/register`
- **Access**: Public (Redirects to `/dashboard/` if already authenticated)
- **Description**: Renders registration form.
- **Response**: `200 OK` (Template: `auth/register.html`)

### `POST /auth/register`
- **Access**: Public
- **Description**: Creates a new student account.
- **Request Form Data**:
  | Field | Type | Required | Description |
  |---|---|---|---|
  | `fullname` | `string` | Yes | Student's full name |
  | `email` | `string` | Yes | Unique email address |
  | `password` | `string` | Yes | Minimum 6 characters |
  | `confirm_password` | `string` | Yes | Must match `password` |
  | `csrf_token` | `string` | Yes | CSRF protection token |
- **Validation**:
  - Checks non-empty fields.
  - Verifies minimum 6-character length for password.
  - Checks password match.
  - Checks for duplicate email in database.
- **Responses**:
  - *Success*: Flash success message -> `302 Redirect` to `/auth/login`
  - *Validation Failure*: Flash danger alert -> Re-renders `auth/register.html`

---

### `GET /auth/login`
- **Access**: Public (Redirects to `/dashboard/` if already authenticated)
- **Description**: Renders the login form.
- **Response**: `200 OK` (Template: `auth/login.html`)

### `POST /auth/login`
- **Access**: Public
- **Description**: Authenticates user credentials and initiates session.
- **Request Form Data**:
  | Field | Type | Required | Description |
  |---|---|---|---|
  | `email` | `string` | Yes | User's registered email |
  | `password` | `string` | Yes | User password |
  | `remember` | `string` | No | Checkbox for persistent cookie session |
  | `csrf_token` | `string` | Yes | CSRF token |
- **Responses**:
  - *Admin Success*: `302 Redirect` to `/admin/`
  - *User Success*: `302 Redirect` to `/dashboard/` (or `?next=` target)
  - *Failure*: Flash danger message -> `auth/login.html`

---

### `GET /auth/logout`
- **Access**: Authenticated (`@login_required`)
- **Description**: Clears user session and terminates authentication.
- **Response**: Flash info alert -> `302 Redirect` to `/auth/login`

---

## Dashboard Blueprint (`main_bp`)

### `GET /dashboard/`
- **Access**: Authenticated (`@login_required`)
- **Description**: Student dashboard displaying summary analytics, category list, and historical scores.
- **Template Context**:
  - `total_quizzes` (`int`): Count of attempts by `current_user`.
  - `avg_score` (`float`): Average percentage score across user attempts.
  - `best_score` (`float`): Maximum percentage score achieved.
  - `categories` (`list`): List of dictionaries containing `id`, `name`, and `question_count`.
  - `recent_attempts` (`list`): Last 5 `QuizAttempt` objects ordered by `completed_at desc`.
- **Response**: `200 OK` (Template: `main/dashboard.html`)

---

## Quiz Engine Blueprint (`quiz_bp`)

### `GET /quiz/categories`
- **Access**: Authenticated (`@login_required`)
- **Description**: Lists all active categories with associated question count badges.
- **Response**: `200 OK` (Template: `quiz/categories.html`)

---

### `GET /quiz/start/<int:category_id>`
- **Access**: Authenticated (`@login_required`)
- **Description**: Initializes an in-memory session quiz instance.
- **Session Variables Initialized**:
  ```python
  session["quiz_category_id"] = category_id
  session["quiz_category_name"] = category.name
  session["quiz_question_ids"] = shuffled_question_ids_list
  session["quiz_answers"] = {}
  session["quiz_current"] = 0
  session["quiz_time_limit"] = config_quiz_time_limit
  session["quiz_start_time"] = current_utc_iso_timestamp
  ```
- **Responses**:
  - *No Questions Available*: Flash warning -> Redirect to `/quiz/categories`
  - *Success*: `302 Redirect` to `/quiz/take`

---

### `GET /quiz/take`
- **Access**: Authenticated (`@login_required`)
- **Description**: Renders active question at index `session["quiz_current"]`.
- **Template Variables**:
  - `question`: Current `Question` object.
  - `current`: 1-based current index.
  - `total`: Total questions count.
  - `selected_answer`: Previously selected option key (`A`, `B`, `C`, or `D`) if any.
  - `is_first` / `is_last`: Navigation booleans.
  - `time_limit`: Duration in seconds.
  - `start_time`: ISO UTC timestamp.
- **Response**: `200 OK` (Template: `quiz/quiz.html`)

---

### `POST /quiz/take`
- **Access**: Authenticated (`@login_required`)
- **Description**: Records option selection and updates question index pointer.
- **Request Form Data**:
  | Field | Type | Required | Description |
  |---|---|---|---|
  | `selected_option` | `string` | No | `A`, `B`, `C`, or `D` |
  | `action` | `string` | Yes | `previous`, `next`, or `submit` |
  | `csrf_token` | `string` | Yes | CSRF token |
- **Responses**:
  - *Previous*: Decrements index -> Redirect to `/quiz/take`
  - *Next*: Increments index -> Redirect to `/quiz/take`
  - *Submit*: Redirect to `/quiz/submit`

---

### `GET` / `POST /quiz/submit`
- **Access**: Authenticated (`@login_required`)
- **Description**: Compares recorded answers against database correct options, inserts `QuizAttempt`, clears active quiz session keys, and stores result in `session["quiz_result"]`.
- **Response**: `302 Redirect` to `/quiz/result`

---

### `GET /quiz/result`
- **Access**: Authenticated (`@login_required`)
- **Description**: Renders score summary and detailed question answer breakdown. Pops `session["quiz_result"]` to prevent stale review access.
- **Response**: `200 OK` (Template: `quiz/result.html`)

---

### `GET /quiz/attempts`
- **Access**: Authenticated (`@login_required`)
- **Description**: Displays full historical table of all past attempts made by the authenticated user.
- **Response**: `200 OK` (Template: `quiz/attempts.html`)

---

## Admin Blueprint (`admin_bp`)

*Note: All endpoints under `/admin` are guarded by `@admin_required`.*

### `GET /admin/`
- **Description**: Global administration overview with metric counters and system breakdown.
- **Metrics**: Total Users, Total Admins, Total Categories, Total Questions, Total Attempts, Platform Average Score, Recent 10 Attempts.
- **Response**: `200 OK` (Template: `admin/dashboard.html`)

---

### `GET /admin/categories`
- **Description**: Category management view listing categories with question counts and category creation form.
- **Response**: `200 OK` (Template: `admin/categories.html`)

### `POST /admin/categories`
- **Description**: Creates a new category entity.
- **Form Data**: `name` (`string`, required)
- **Response**: Flash status -> `302 Redirect` to `/admin/categories`

### `POST /admin/categories/delete/<int:category_id>`
- **Description**: Deletes target category and all linked questions + attempt records via cascade delete.
- **Response**: Flash success -> `302 Redirect` to `/admin/categories`

---

### `GET /admin/questions`
- **Description**: Browse all questions with optional category filtering (`?category_id=<int>`).
- **Response**: `200 OK` (Template: `admin/questions.html`)

### `GET /admin/questions/add`
- **Description**: Renders question creation form.
- **Response**: `200 OK` (Template: `admin/add_question.html`)

### `POST /admin/questions/add`
- **Description**: Inserts a new MCQ question.
- **Form Data**:
  - `category_id` (`int`)
  - `question` (`text`)
  - `option_a`, `option_b`, `option_c`, `option_d` (`string`)
  - `correct_option` (`string`: `A`, `B`, `C`, or `D`)
- **Response**: Flash success -> `302 Redirect` to `/admin/questions`

### `GET /admin/questions/edit/<int:question_id>`
- **Description**: Renders edit form populated with current question attributes.
- **Response**: `200 OK` (Template: `admin/edit_question.html`)

### `POST /admin/questions/edit/<int:question_id>`
- **Description**: Updates existing question record in database.
- **Response**: Flash success -> `302 Redirect` to `/admin/questions`

### `POST /admin/questions/delete/<int:question_id>`
- **Description**: Permanently removes a question entity.
- **Response**: Flash success -> `302 Redirect` to `/admin/questions`

---

### `GET /admin/users`
- **Description**: Lists all registered users and timestamps.
- **Response**: `200 OK` (Template: `admin/users.html`)

---

### `GET /admin/attempts`
- **Description**: Displays global log of all quiz attempts across all users in descending order.
- **Response**: `200 OK` (Template: `admin/attempts.html`)

---

## Error Handling & Redirect Semantics

| Scenario | HTTP / Application Behavior | User Feedback |
|---|---|---|
| Unauthenticated Access to Protected Route | `302 Found` -> `/auth/login?next=<requested_path>` | Warning flash: *"Please log in to access this page."* |
| Non-Admin Access to `/admin/*` | `302 Found` -> `/dashboard/` | Danger flash: *"Access denied. Admin privileges required."* |
| Entity Not Found (`404`) | `404 Not Found` handled by Flask | Standard 404 response |
| Missing Quiz Session | `302 Found` -> `/quiz/categories` | Warning flash: *"No active quiz session."* |
