"""
This module initializes the database models and imports necessary modules.

It follows the Flask application factory pattern to prevent circular dependencies.
"""

# this file structure follows http://flask.pocoo.org/docs/1.0/patterns/appfactories/
# initializing db in __init__.py
# to prevent circular dependencies

from {{cookiecutter.project_slug}}.models import Module, Log
from {{cookiecutter.project_slug}}.extensions import db

__all__ = ['db', 'Module', 'Log']
