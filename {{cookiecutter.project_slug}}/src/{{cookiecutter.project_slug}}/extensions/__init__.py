from celery import Celery
from flasgger import Swagger
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .S3 import S3Storage

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
celery = Celery(__name__, broker='')
swagger = Swagger()
S3Storage()
