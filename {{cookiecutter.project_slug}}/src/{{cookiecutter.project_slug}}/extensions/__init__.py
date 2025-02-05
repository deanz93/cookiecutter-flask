from celery import Celery
{% if cookiecutter.use_swagger == 'y' %}from flasgger import Swagger{% endif %}
from flask_cors import CORS
{% if cookiecutter.use_email_service == 'y' %}from flask_mail import Mail{% endif %}
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
{% if cookiecutter.use_cloud_storage == 'y' %}from .S3 import S3Storage{% endif %}
{% if cookiecutter.authentication_type == "Firebase" %}from .firebase import Firebase{% endif %}

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
celery = Celery(__name__, broker='')
{% if cookiecutter.use_swagger == 'y' %}swagger = Swagger(){% endif %}
{% if cookiecutter.use_email_service == 'y' %}mail = Mail(){% endif %}
{% if cookiecutter.use_cloud_storage == 'y' %}S3Storage(){% endif %}
{% if cookiecutter.authentication_type == "Firebase" %}Firebase(){% endif %}
