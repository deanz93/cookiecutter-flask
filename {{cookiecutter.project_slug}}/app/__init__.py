from flask import Flask
from .extensions import db, migrate, cors{% if cookiecutter.use_swagger == 'y' %}, swagger{% endif %}{% if cookiecutter.use_celery == 'y' %}, celery{% endif %}
from .config import Config
from . import views

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    {% if cookiecutter.use_swagger == 'y' %}swagger.init_app(app){% endif %}
    {% if cookiecutter.use_celery == 'y' %}# Initialize Celery
    celery.conf.update(app.config){% endif %}

    app.register_blueprint(views.bp)

    return app