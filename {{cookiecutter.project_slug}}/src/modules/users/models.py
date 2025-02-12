"""
This module defines the database models for users in the application.

The models defined here include:
- User: Represents a user with personal details, authentication info, and other attributes.
- Organization: Represents an organization with details, related to a user as admin.
"""
import uuid
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from database.core import Mixin
from {{ cookiecutter.project_slug }}.extensions import db


class User(Mixin, db.Model, UserMixin):
    """Person Table."""

    __tablename__ = "person"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    picture = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, default=True, nullable=False)
    is_super_admin = db.Column(db.Boolean, default=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=func.now(), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    signed_in_provider = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, active, display_name, email, signed_in_provider,
                 is_admin, is_super_admin, date_joined, password=None,
                 picture=None, date_of_birth=None, phone_number=None,
                 user_id=None):
        if user_id:
            self.id = user_id
        self.display_name = display_name
        self.active = active
        self.is_admin = is_admin
        self.is_super_admin = is_super_admin
        self.email = email
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.signed_in_provider = signed_in_provider
        self.date_joined = date_joined
        self.picture = picture
        if password:
            self.set_password(password)

    def save(self):
        """Save the user instance to the database."""
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password = generate_password_hash(password, method='pbkdf2:sha512')

    def check_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password, password)

    def is_active(self):
        """Return True if the user is active."""
        return self.active

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
        return f"<Organization {self.organization_email}>"
