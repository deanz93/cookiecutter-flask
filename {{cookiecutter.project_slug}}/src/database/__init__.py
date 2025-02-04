"""
This module initializes the database models and imports necessary modules.

It follows the Flask application factory pattern to prevent circular dependencies.
"""

# this file structure follows http://flask.pocoo.org/docs/1.0/patterns/appfactories/
# initializing db in __init__.py
# to prevent circular dependencies

from my_flask_app.models import Module, Log
from my_flask_app.extensions import db

__all__ = ['db', 'Module', 'Log']
