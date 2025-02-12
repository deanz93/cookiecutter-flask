"""
Instance-specific configurations for the Flask application.
"""
import ast
import os
import pytz
{% if cookiecutter.use_swagger == 'y' %}
from {{ cookiecutter.project_slug }}.extensions.flasgger import requires_basic_auth, requires_bearer_auth
{% endif %}

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
    TESTING = ast.literal_eval(
        os.getenv('FLASK_TESTING', 'False'))
    TEMPLATES_AUTO_RELOAD = True
{% if cookiecutter.use_cloud_storage == 'y' %}
    # Cloud Storage
    USE_S3 = ast.literal_eval(
        os.getenv("USE_S3", 'False')
    )
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_ENDPOINT = os.getenv("S3_ENDPOINT")
    S3_REGION = os.getenv("S3_REGION")
    S3_BUCKET = os.getenv("S3_BUCKET")
{% endif %}
    # JWT conf
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = os.getenv("JWT_TOKEN_LOCATION", "cookies")
    JWT_COOKIE_SECURE = ast.literal_eval(
        os.getenv("JWT_COOKIE_SECURE"))

    SESSION_TYPE = os.getenv("SESSION_TYPE")
    SESSION_PERMANENT = ast.literal_eval(
        os.getenv("SESSION_PERMANENT"))
    SESSION_USE_SIGNER = ast.literal_eval(
        os.getenv("SESSION_USE_SIGNER"))
    SESSION_KEY_PREFIX = os.getenv("SESSION_KEY_PREFIX")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
{% if cookiecutter.use_email_service == 'y' %}
    email_enable = ast.literal_eval(
        os.getenv('EMAIL_ENABLE', 'False'))

    if email_enable:
        MAIL_SERVER = os.getenv("MAIL_SERVER", 'localhost')
        MAIL_DEBUG = ast.literal_eval(
            os.getenv('MAIL_DEBUG', 'True'))
        MAIL_PORT = int(os.getenv("MAIL_PORT", '25'))
        MAIL_USE_TLS = ast.literal_eval(
            os.getenv('MAIL_USE_TLS', 'True'))
        MAIL_USE_SSL = ast.literal_eval(
            os.getenv('MAIL_USE_SSL', 'False'))
        MAIL_USERNAME = os.getenv("MAIL_USERNAME", '')
        MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", '')
        MAIL_DEFAULT_SENDER = os.getenv("DEFAULT_FROM_EMAIL")
{% endif %}
    # CORS
    CORS_HEADERS = 'Content-Type'
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*')  # e.g., 'https://example.com'
    {% if cookiecutter.use_celery == 'y' %}# Redis Settings
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    # Celery Settings
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'){% endif %}
{% if cookiecutter.use_swagger == 'y' %}
    SWAGGER = {
        "openapi": "3.0.2",
        "info": {
            'title': '{{ cookiecutter.project_name }} API',
            "version": "1.0.0",
        },
        "components": {
            "securitySchemes": {
                "BasicAuth": {
                    "type": "http",
                    "scheme": "basic"
                },
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"  # Optional but helps with UI clarity
                }
            }
        },
        "security": [
            {"BasicAuth": []},
            {"BearerAuth": []}
        ]
    }{% endif %}

    # Timezone Settings
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
{% if cookiecutter.authentication_type == "Firebase" %}
    DEFAULT_GOOGLE_SDK_FILEPATH = os.path.join(os.path.dirname(__file__), "google-credentials.json")
    GOOGLE_CREDENTIALS_FILEPATH = os.getenv(
        "GOOGLE_CREDENTIALS_FILEPATH",
        default=DEFAULT_GOOGLE_SDK_FILEPATH)
{% endif %}
