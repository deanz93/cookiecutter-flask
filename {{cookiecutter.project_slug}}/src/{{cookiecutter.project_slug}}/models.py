from datetime import datetime

from database.core import Mixin
from .extensions import db

class Module(Mixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    version = db.Column(db.String(20), default='1.0.0')  # Versioning
    enabled = db.Column(db.Boolean, default=False)
    installed_at = db.Column(db.DateTime, default=datetime.utcnow)

class Log(Mixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    module_name = db.Column(db.String(50))