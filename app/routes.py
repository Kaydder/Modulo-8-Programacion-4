"""Flask routes for the personal library application."""
from __future__ import annotations

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from .extensions import db
from .models import Book
from .tasks import send_book_notification

library_bp = Blueprint("library", __name__)


@library_bp.route("/")
def index():
    books = Book.query.order_by(Book.created_at.desc()).all()
    recipient = (
        current_app.config.get("LIBRARY_NOTIFICATION_EMAIL")
        or current_app.config.get("MAIL_USERNAME")
    )
    return render_template("index.html", books=books, recipient=recipient)


@library_bp.route("/books", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    recipient = request.form.get("recipient", "").strip() or None

    if not title or not author:
        flash("El título y el autor son obligatorios", "error")
        return redirect(url_for("library.index"))

    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()

    send_book_notification.delay(
        "agregado",
        {"title": book.title, "author": book.author, "recipient": recipient},
    )

    flash(f"Se agregó '{book.title}'", "success")
    return redirect(url_for("library.index"))


@library_bp.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id: int):
    book = Book.query.get_or_404(book_id)
    recipient = request.form.get("recipient", "").strip() or None

    db.session.delete(book)
    db.session.commit()

    send_book_notification.delay(
        "eliminado",
        {"title": book.title, "author": book.author, "recipient": recipient},
    )

    flash(f"Se eliminó '{book.title}'", "success")
    return redirect(url_for("library.index"))
