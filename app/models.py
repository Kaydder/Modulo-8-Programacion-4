"""Database models."""
from __future__ import annotations

from datetime import datetime

from .extensions import db


class Book(db.Model):
    """Book stored in the personal library."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover - repr for debugging
        return f"<Book {self.title!r} by {self.author!r}>"
