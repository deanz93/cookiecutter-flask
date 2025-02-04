import click
import os
from database import __all__
from database.seeder import seed_database
from flask import Flask
from flask.cli import AppGroup
from modules.manager.urls import module_blueprint
from sqlalchemy_utils import create_database, database_exists
from .extensions import db, migrate, cors{% if cookiecutter.use_swagger == 'y' %}, swagger{% endif %}{% if cookiecutter.use_celery == 'y' %}, celery{% endif %}
from .config import Config
from . import views


def create_app(config_class=Config):
    app = Flask(__name__, root_path=os.path.join(os.getcwd()),
                instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)

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