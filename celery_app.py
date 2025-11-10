"""Celery application used to execute asynchronous tasks."""
from __future__ import annotations

from app import create_app
from app.celery_utils import celery, init_celery

app = create_app()
init_celery(app)
