import uuid
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash

from database.core import Mixin
from {{ cookiecutter.project_slug }}.extensions import db


class User(Mixin, db.Model):
    """Person Table."""

    __tablename__ = "person"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    picture = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=func.now(), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    signed_in_provider = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, active, first_name, last_name, email, password, date_of_birth, phone_number, signed_in_provider, picture=None):
        self.first_name = first_name
        self.last_name = last_name
        self.active = active
        self.email = email
        self.password = generate_password_hash(password)
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.signed_in_provider = signed_in_provider
        self.picture = picture

    def save(self):
        if not self.password.startswith('pbkdf2:sha256'):
            self.password = generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return self.password == generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.email}>"


class Organization(Mixin, db.Model):
    """Organization Table."""

    __tablename__ = "person_organization"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(150), nullable=False)
    organization_email = db.Column(db.String(150), unique=True, nullable=False)
    picture = db.Column(db.String(255))
    admin_id = db.Column(db.String(36), db.ForeignKey('person.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    admin = db.relationship('User', backref='organizations', cascade="all")

    def __repr__(self):
        return f"<User {self.organization_email}>"