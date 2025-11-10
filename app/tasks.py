"""Celery tasks used by the personal library application."""
from __future__ import annotations

from typing import Any

from flask import current_app
from flask_mail import Message

from .celery_utils import celery
from .extensions import mail


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def send_book_notification(self, action: str, book_data: dict[str, Any]) -> None:
    """Send an email notification for a book action."""

    app = current_app._get_current_object()  # type: ignore[attr-defined]
    recipient = (
        book_data.get("recipient")
        or app.config.get("LIBRARY_NOTIFICATION_EMAIL")
        or app.config.get("MAIL_USERNAME")
    )

    if not recipient:
        app.logger.warning("No recipient configured for book notifications")
        return

    subject = f"Library update: book {action}"
    body = (
        "Hola,\n\n"
        f"El libro '{book_data.get('title')}' de {book_data.get('author')} "
        f"ha sido {action} en tu biblioteca personal.\n"
        "\nSaludos,\nTu biblioteca personal"
    )

    message = Message(subject=subject, recipients=[recipient], body=body)
    mail.send(message)
