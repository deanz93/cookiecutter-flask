"""
This module handles the registration of the module's blueprint.

The `register` function is responsible for returning the module's blueprint
to be registered with a Flask application. This allows the application to
include routes and views defined in this module.

Modules can use this setup to extend and integrate additional functionality into
the main application by providing their own blueprints.

Imports:
    module_blueprint (module): The blueprint instance for the module's routes.

Functions:
    register() -> Blueprint: Returns the module's blueprint for registration.
"""
from .urls import users_blueprint


def register():
    """
    Registers the module's blueprint for the application.

    Returns:
        Blueprint: The module's blueprint to be registered with the app.
    """

    return users_blueprint
