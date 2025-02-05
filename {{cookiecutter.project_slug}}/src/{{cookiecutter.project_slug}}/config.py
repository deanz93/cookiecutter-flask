"""
Instance-specific configurations for the Flask application.
"""
import ast
import os
import pytz


class Config:
    """
    Configuration settings for the Flask application.
    """
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
    tz = pytz.timezone(TIMEZONE)

    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False')
    UPLOAD_FOLDER = os.path.abspath(os.getenv("UPLOAD_FOLDER", 'uploads'))
    OUTPUT_FOLDER = os.path.abspath(os.getenv("OUTPUT_FOLDER", 'generated'))
    STATIC_PATH = os.path.abspath(os.getenv("STATIC_PATH", 'staticfiles'))
    TESTING = os.getenv('FLASK_TESTING', 'False')
    TEMPLATES_AUTO_RELOAD = True
    {% if cookiecutter.use_cloud_storage == 'y' %}
    # Cloud Storage
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_ENDPOINT = os.getenv("S3_ENDPOINT")
    S3_REGION = os.getenv("S3_REGION")
    S3_BUCKET = os.getenv("S3_BUCKET")
    {% endif %}
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    {% if cookiecutter.use_email_service == 'y' %}
    MAIL_SERVER = os.getenv("MAIL_SERVER", 'localhost')
    MAIL_PORT = int(os.getenv("MAIL_PORT", '25'))
    MAIL_USE_TLS = ast.literal_eval(
        os.getenv('MAIL_USE_TLS', 'True'))
    MAIL_USE_SSL = ast.literal_eval(
        os.getenv('MAIL_USE_SSL', 'False'))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", '')
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", '')
    MAIL_DEFAULT_SENDER = os.getenv("DEFAULT_FROM_EMAIL"){% endif %}

    # CORS
    CORS_HEADERS = 'Content-Type'
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*')  # e.g., 'https://example.com'

    {% if cookiecutter.use_celery == 'y' %}# Redis Settings
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    # Celery Settings
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'){% endif %}

    {% if cookiecutter.use_swagger == 'y' %}SWAGGER = {
        'title': '{{ cookiecutter.project_name }} API',
        'uiversion': 3,
        'openapi': '3.0.2'
    }{% endif %}

    # Timezone Settings
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
