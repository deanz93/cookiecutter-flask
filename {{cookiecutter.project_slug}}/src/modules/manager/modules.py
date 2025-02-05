from .urls import module_blueprint


def register(app):
    app.register_blueprint(module_blueprint, url_prefix='/module')
