"""Application factory for the personal library project."""
from __future__ import annotations

from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

from .config import Config
from .extensions import db, mail
from .celery_utils import init_celery


def create_app(config_class: type[Config] | None = None) -> Flask:
    """Create and configure the Flask application."""

    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class or Config)

    db.init_app(app)
    mail.init_app(app)

    Migrate(app, db)

    from .routes import library_bp

    app.register_blueprint(library_bp)

    with app.app_context():
        db.create_all()

    init_celery(app)

    return app
