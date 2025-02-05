{% if cookiecutter.use_celery == 'y' %}from celery import Celery{% endif %}
{% if cookiecutter.use_swagger == 'y' %}from flasgger import Swagger{% endif %}
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
{% if cookiecutter.use_celery == 'y' %}celery = Celery(__name__, broker=''){% endif %}
{% if cookiecutter.use_swagger == 'y' %}swagger = Swagger(){% endif %}
