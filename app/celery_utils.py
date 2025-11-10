"""Celery helpers for the personal library application."""
from __future__ import annotations

from celery import Celery
from flask import Flask

celery = Celery(__name__)


def init_celery(app: Flask) -> Celery:
    """Configure Celery to work with the given Flask application."""

    existing = app.extensions.get("celery")
    if existing:
        return existing

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        task_ignore_result=True,
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
    app.extensions["celery"] = celery
    return celery
