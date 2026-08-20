"""
BrainCheck - Flask Quiz App
Sets up the app, connects extensions, and seeds the database on first run.
"""

import os
from flask import Flask, redirect, url_for
from extensions import db, login_manager, csrf
from werkzeug.security import generate_password_hash
from config import Config


def create_app(config_class=Config):
    """Creates and returns the Flask application."""

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    from models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.quiz import quiz_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def index():
        return redirect(url_for("main.dashboard"))

    with app.app_context():
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
        if db_uri and db_uri.startswith("sqlite:///"):
            db_path = db_uri.replace("sqlite:///", "")
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
        db.create_all()
        _seed_defaults(app)

    return app


def _seed_defaults(app):
    """Seeds the database with default admin account and sample questions."""

    from models.models import User, QuizCategory, Question

    # create admin if not already there
    if not User.query.filter_by(email="admin@braincheck.com").first():
        admin = User(
            fullname="Admin",
            email="admin@braincheck.com",
            password_hash=generate_password_hash(
                os.environ.get("ADMIN_PASSWORD", "Admin@123")
            ),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()

    sample_categories = ["Python", "JavaScript", "Docker", "General Knowledge"]
    for name in sample_categories:
        if not QuizCategory.query.filter_by(name=name).first():
            db.session.add(QuizCategory(name=name))
    db.session.commit()

    python_cat = QuizCategory.query.filter_by(name="Python").first()
    if python_cat and Question.query.filter_by(category_id=python_cat.id).count() == 0:
        questions = [
            Question(
                category_id=python_cat.id,
                question="What is the output of print(type([]))?",
                option_a="<class 'list'>",
                option_b="<class 'tuple'>",
                option_c="<class 'dict'>",
                option_d="<class 'set'>",
                correct_option="A",
            ),
            Question(
                category_id=python_cat.id,
                question="Which keyword is used to define a function in Python?",
                option_a="function",
                option_b="def",
                option_c="func",
                option_d="define",
                correct_option="B",
            ),
            Question(
                category_id=python_cat.id,
                question="What does PEP stand for?",
                option_a="Python Enhancement Proposal",
                option_b="Python Evaluation Process",
                option_c="Python Extension Package",
                option_d="Python Execution Plan",
                correct_option="A",
            ),
            Question(
                category_id=python_cat.id,
                question="Which data type is immutable in Python?",
                option_a="List",
                option_b="Dictionary",
                option_c="Set",
                option_d="Tuple",
                correct_option="D",
            ),
            Question(
                category_id=python_cat.id,
                question="What is the default return value of a Python function?",
                option_a="0",
                option_b="None",
                option_c="False",
                option_d="Empty string",
                correct_option="B",
            ),
        ]
        db.session.add_all(questions)
        db.session.commit()

    docker_cat = QuizCategory.query.filter_by(name="Docker").first()
    if docker_cat and Question.query.filter_by(category_id=docker_cat.id).count() == 0:
        questions = [
            Question(
                category_id=docker_cat.id,
                question="What is a Docker container?",
                option_a="A virtual machine",
                option_b="A lightweight, standalone executable package",
                option_c="A programming language",
                option_d="A database engine",
                correct_option="B",
            ),
            Question(
                category_id=docker_cat.id,
                question="Which file defines a Docker image?",
                option_a="docker-compose.yml",
                option_b="Makefile",
                option_c="Dockerfile",
                option_d="requirements.txt",
                correct_option="C",
            ),
            Question(
                category_id=docker_cat.id,
                question="What command builds a Docker image?",
                option_a="docker run",
                option_b="docker build",
                option_c="docker create",
                option_d="docker start",
                correct_option="B",
            ),
            Question(
                category_id=docker_cat.id,
                question="Which command lists running Docker containers?",
                option_a="docker images",
                option_b="docker ps",
                option_c="docker list",
                option_d="docker show",
                correct_option="B",
            ),
            Question(
                category_id=docker_cat.id,
                question="What does docker-compose do?",
                option_a="Compiles Docker images",
                option_b="Defines and runs multi-container applications",
                option_c="Monitors container health",
                option_d="Encrypts container data",
                correct_option="B",
            ),
        ]
        db.session.add_all(questions)
        db.session.commit()

    js_cat = QuizCategory.query.filter_by(name="JavaScript").first()
    if js_cat and Question.query.filter_by(category_id=js_cat.id).count() == 0:
        questions = [
            Question(
                category_id=js_cat.id,
                question="Which company developed JavaScript?",
                option_a="Microsoft",
                option_b="Netscape",
                option_c="Google",
                option_d="Apple",
                correct_option="B",
            ),
            Question(
                category_id=js_cat.id,
                question="What does 'typeof null' return in JavaScript?",
                option_a="null",
                option_b="undefined",
                option_c="object",
                option_d="boolean",
                correct_option="C",
            ),
            Question(
                category_id=js_cat.id,
                question="Which symbol is used for single-line comments in JavaScript?",
                option_a="#",
                option_b="//",
                option_c="--",
                option_d="/* */",
                correct_option="B",
            ),
            Question(
                category_id=js_cat.id,
                question="What is the correct way to declare a constant in JavaScript?",
                option_a="var x = 5",
                option_b="let x = 5",
                option_c="const x = 5",
                option_d="constant x = 5",
                correct_option="C",
            ),
            Question(
                category_id=js_cat.id,
                question="Which method converts a JSON string to a JavaScript object?",
                option_a="JSON.stringify()",
                option_b="JSON.parse()",
                option_c="JSON.toObject()",
                option_d="JSON.convert()",
                correct_option="B",
            ),
        ]
        db.session.add_all(questions)
        db.session.commit()

    gk_cat = QuizCategory.query.filter_by(name="General Knowledge").first()
    if gk_cat and Question.query.filter_by(category_id=gk_cat.id).count() == 0:
        questions = [
            Question(
                category_id=gk_cat.id,
                question="What is the largest planet in our solar system?",
                option_a="Earth",
                option_b="Mars",
                option_c="Jupiter",
                option_d="Saturn",
                correct_option="C",
            ),
            Question(
                category_id=gk_cat.id,
                question="Which element has the chemical symbol 'O'?",
                option_a="Gold",
                option_b="Oxygen",
                option_c="Osmium",
                option_d="Iron",
                correct_option="B",
            ),
            Question(
                category_id=gk_cat.id,
                question="In which year did World War II end?",
                option_a="1943",
                option_b="1944",
                option_c="1945",
                option_d="1946",
                correct_option="C",
            ),
            Question(
                category_id=gk_cat.id,
                question="What is the capital of Japan?",
                option_a="Seoul",
                option_b="Beijing",
                option_c="Bangkok",
                option_d="Tokyo",
                correct_option="D",
            ),
            Question(
                category_id=gk_cat.id,
                question="How many continents are there on Earth?",
                option_a="5",
                option_b="6",
                option_c="7",
                option_d="8",
                correct_option="C",
            ),
        ]
        db.session.add_all(questions)
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", os.environ.get("PORT", 5000))),
        debug=os.environ.get("FLASK_DEBUG", "False").lower() == "true",
    )
