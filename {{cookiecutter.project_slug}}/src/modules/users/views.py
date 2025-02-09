"""
This module contains functions for creating users and sending registration emails.

Functions:

    - create_user: Create a new user and send a registration email.
"""
import os
from flask import current_app
from flask_mail import Message

from {{ cookiecutter.project_slug }}.extensions import mail
from modules.users.models import User


def create_user(first_name, last_name, email, picture, password, date_of_birth, phone_number, signed_in_provider):
    """
    Create a new user and send a registration email.

    Args:
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): User's email address.
        picture (str): User's profile picture URL.
        password (str): User's password.
        date_of_birth (datetime.date): User's date of birth.
        phone_number (str): User's phone number.
        signed_in_provider (str): User's signed-in provider.

    Returns:
        dict: A dictionary containing the status of the registration,
            a message and a status code.
    """
    is_exist = User.query.filter_by(email=email).first()

    if is_exist:
        absolute_dir = os.path.dirname(os.path.abspath(__file__))

        account_already_exists_message_template = 'account_already_exists_message.txt'
        path_to_email_template = os.path.join(absolute_dir, 'templates', 'email',
                                              account_already_exists_message_template)

        with open(path_to_email_template, 'r', encoding='utf-8') as file:
            body = file.read()

        body = body.format(
            app_name=current_app.name,
            email=email,
        )
        # send email reminder user
        try:
            msg = Message(
                subject='Account Already Exists',
                recipients=[email],
                body=body,
                sender=os.getenv('DEFAULT_FROM_EMAIL')
            )
            print(mail)
            mail.send(msg)
        except Exception as e:
            print(e)
        return {'status': False, 'message': "Unable to register user.", 'code': 200}

    user = User(
        password=password,
        active=True,  # Assuming new users are active by default
        first_name=first_name,
        last_name=last_name,
        email=email,
        date_of_birth=date_of_birth,
        phone_number=phone_number,
        signed_in_provider=signed_in_provider,
        picture=picture,
    )

    try:
        user.save()
        return {'status': True, 'message': f"User {email} registered successfully.", 'code': 201}
    except Exception as e:
        return {'status': False, 'message': f"An error occurred during registration. {e}", 'code': 500}
