import importlib
import os

import click
from flask import Flask
from flask.cli import AppGroup
from sqlalchemy_utils import create_database, database_exists

from database.auto_discover_models import auto_load_models
from database.seeder import seed_database
from modules.manager.models import Module
from modules.manager.views import create_module


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

    # Inpired from Django's installed_apps. Register when you develop a new module
    # Uploaded modules don't need to be registered here; they will be loaded automatically when enabled in the manager.
    installed_apps = [
        'manager',
    ]

    load_modules(app, installed_apps)

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
    # app.register_blueprint(module_blueprint, url_prefix='/module')

    seed_cli = AppGroup('database')
    generate_module = AppGroup("module")

    # Flask CLI command
    @seed_cli.command('seed')
    @click.option('--replace', is_flag=True, help='Clear existing data before seeding.')
    def run_seed(replace):
        """
        Run the database seeder.

        Args:
            replace (bool): If True, clear existing data before seeding.
        """
        seed_database(replace=replace)

    @seed_cli.command('auto_discover')
    def run_auto_load_models():
        auto_load_models(installed_apps)

    @generate_module.command("generate")
    @click.option('--name', required=True, help="The desired name for the new module, used for the models file.")
    def generate_new_module(name):
        """
        Create a new module in the specified directory with the given name.

        Args:
            name (str): Name of the module, which will be capitalized.

        Returns:
            None
        """
        create_module(name)

    app.cli.add_command(seed_cli)
    app.cli.add_command(generate_module)

    return app


def load_modules(app, installed_apps=[]):
    modules_dir = 'modules'

    if len(installed_apps) > 0:
        for module_name in installed_apps:
            try:
                module = importlib.import_module(f'modules.{module_name}.modules')
                if hasattr(module, 'register'):
                    app.register_blueprint(module.register())
                    importlib.reload(module)
            except Exception as e:
                print(e)

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
