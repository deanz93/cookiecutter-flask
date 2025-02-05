"""
This module defines the database models for the application.

The models defined here include:
- Module: Represents a module which can be installed and enabled/disabled.
- Log: Represents a log entry with details about events or actions.
"""

from sqlalchemy.sql import func

from database.core import Mixin
from {{cookiecutter.project_slug}}.extensions import db


class Module(Mixin, db.Model):
    """
    Module model.

    This model represents a module which can be installed and enabled/disabled.
    """
    __tablename__ = "general_modules"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    version = db.Column(db.String(20), default='1.0.0')  # Versioning
    enabled = db.Column(db.Boolean, default=False)
    installed_at = db.Column(db.DateTime, default=func.now())
    created_at = db.Column(db.DateTime, server_default=func.now())  # Timestamp for creation
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())  # Timestamp for updates


class Log(Mixin, db.Model):
    """
    Log model.

    This model represents a log entry for a module.
    """
    __tablename__ = "general_modules_logs"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())
    module_name = db.Column(db.String(50))
