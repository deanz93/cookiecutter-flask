import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*')
    {% if cookiecutter.use_redis == 'y' %}REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0'){% endif %}
    {% if cookiecutter.use_celery == 'y' %}
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'){% endif %}
    {% if cookiecutter.use_swagger == 'y' %}
    SWAGGER = {
        'title': '{{ cookiecutter.project_name }} API',
        'uiversion': 3,
        'openapi': '3.0.2'
    }{% endif %}