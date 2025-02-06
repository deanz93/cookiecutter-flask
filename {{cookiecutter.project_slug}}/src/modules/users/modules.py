from .urls import users_blueprint


def register():
    """
    Registers the module's blueprint for the application.

    Returns:
        Blueprint: The module's blueprint to be registered with the app.
    """

    return users_blueprint
    # app.register_blueprint(module_blueprint, url_prefix='/module')
