import importlib
import os

import click
from flask import Flask
from flask.cli import AppGroup
from sqlalchemy_utils import create_database, database_exists

from database.seeder import seed_database
from modules.manager.models import Module
from modules.manager.urls import module_blueprint

from . import views
from .config import Config
from .extensions import (
    {% if cookiecutter.use_celery == 'y' %}celery,{% endif %}
    cors,
    db,
    migrate,
    {% if cookiecutter.use_swagger == 'y' %}swagger,{% endif %}
    {% if cookiecutter.use_email_service == 'y' %}mail,{% endif %}
    {% if cookiecutter.use_cloud_storage == 'y' %}s3,{% endif %}
    {% if cookiecutter.authentication_type == "Firebase" %}firebase,{% endif %}
    )


def create_app(config_class=Config):
    app = Flask(__name__, root_path=os.path.join(os.getcwd()),
                instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    load_modules(app)

    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        print("db not exist. Creating..")
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(app.config['STATIC_PATH'], exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/*": {"origins": app.config['ALLOWED_ORIGINS']}})

    {% if cookiecutter.use_swagger == 'y' %}swagger.init_app(app){% endif %}
    {% if cookiecutter.use_celery == 'y' %}# Initialize Celery
    celery.conf.update(app.config){% endif %}

    {% if cookiecutter.use_cloud_storage == 'y' %}# Initialize the S3 extension
    s3.init_app(app){% endif %}
    {% if cookiecutter.use_email_service == 'y' %}# Initialize the Mail
    mail.init_app(app){% endif %}

    {% if cookiecutter.authentication_type == "Firebase" %}firebase.init_app(app){% endif %}

    app.register_blueprint(views.bp)
    app.register_blueprint(module_blueprint, url_prefix='/module')

    seed_cli = AppGroup('seed')

    # Flask CLI command
    @seed_cli.command('run')
    @click.option('--replace', is_flag=True, help='Clear existing data before seeding.')
    def run_seed(replace):
        """
        Run the database seeder.

        Args:
            replace (bool): If True, clear existing data before seeding.
        """
        seed_database(replace=replace)

    app.cli.add_command(seed_cli)

    return app


def load_modules(app):
    modules_dir = 'modules'

    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name)
        with app.app_context():
            if os.path.isdir(module_path) and os.path.exists(os.path.join(module_path, '__init__.py')):
                module_entry = Module.query.filter_by(name=module_name, enabled=True).first()
                if module_entry:
                    module = importlib.import_module(f'modules.{module_name}.modules')
                    if hasattr(module, 'register'):
                        app.register_blueprint(module.register())
                        importlib.reload(module)
