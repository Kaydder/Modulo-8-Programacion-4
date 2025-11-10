"""Application extensions initialised without app context."""
from __future__ import annotations

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mail = Mail()
