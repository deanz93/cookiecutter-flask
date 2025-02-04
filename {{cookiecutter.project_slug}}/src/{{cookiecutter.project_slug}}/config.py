"""
Instance-specific configurations for the Flask application.
"""
import os

class Config:
    """
    Configuration settings for the Flask application.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    TESTING = os.getenv('FLASK_TESTING', 'False') == 'True'
    TEMPLATES_AUTO_RELOAD = True

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS
    CORS_HEADERS = 'Content-Type'
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*')  # e.g., 'https://example.com'

    {% if cookiecutter.use_redis == 'y' %}# Redis Settings
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    {% endif %}
    {% if cookiecutter.use_celery == 'y' %}# Celery Settings
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'){% endif %}

    {% if cookiecutter.use_swagger == 'y' %}SWAGGER = {
        'title': '{{ cookiecutter.project_name }} API',
        'uiversion': 3,
        'openapi': '3.0.2'
    }{% endif %}

    # Timezone Settings
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')