"""
This module provides endpoints for user authentication.

Endpoints:
    - /signin: Sign in and return a JWT token.

Imports:
    - flask: A web framework for Python.
    - flasgger: A library for generating Swagger documentation.
"""

from datetime import timedelta
from flasgger import swag_from
from flask import Blueprint, request, render_template, jsonify, redirect, session, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, unset_jwt_cookies
from flask_login import login_user, logout_user

from {{ cookiecutter.project_slug }}.extensions import login_manager
from modules.users.models import User
from modules.users.views import create_user

users_blueprint = Blueprint(
    "users", __name__, template_folder="templates", url_prefix="/users"
)


@login_manager.user_loader
def load_user(user_id):
    """
    This function is used by Flask-Login to load a user by their id.

    Args:
        user_id (int): The id of the user to load.

    Returns:
        A User object, or None if no user with the given id could be found.
    """
    return User.query.get(user_id)


@users_blueprint.route("/login/", methods=["POST", "GET"])
def login():
    """
    Sign in
    ---
    tags:
      - Authentication
    consumes:
        - application/json
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
                format: email
                description: Email address.
                example: alice@example.com
              password:
                type: string
                description: Password.
                example: secret
    responses:
        200:
            description: OK.
        401:
            description: User is not able to sign in.
    """
    if request.method == "GET":
        # Serve the login page for web users
        return render_template("login.html")

    # Check if the request is JSON (API)
    if request.is_json:
        data = request.get_json()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
    else:
        # Handle form submission (Session-based)
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Check if the user is enabled
        if user.active:
            if request.is_json:
                expires_delta = timedelta(hours=1)
                access_token = create_access_token(identity=user.id, expires_delta=expires_delta)
                refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=5))

                response = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": expires_delta.total_seconds(),  # Expiry time in seconds
                    "token_type": "Bearer"
                }
                set_access_cookies(response, access_token)

                return jsonify(), 200

            login_user(user)  # Start a session
            session["user_id"] = user.id  # Store in session

            # Web request → Redirect to dashboard (or any page)
            return redirect(url_for("modules.module"))

        else:
            return jsonify({"message": "User is disabled."}), 401
    else:
        return jsonify({"message": "Invalid email or password."}), 401


@users_blueprint.route("/register/", methods=["POST"])
def register_user():
    """
    Register new user
    ---
    tags:
      - users
    consumes:
        - application/json
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              first_name:
                type: string
                description: First name.
                example: Alice
              last_name:
                type: string
                description: Last name.
                example: Smith
              email:
                type: string
                format: email
                description: Email address.
                example: alice@example.com
              picture:
                type: string
                description: Profile picture URL.
                example: https://example.com/alice.jpg
              password:
                type: string
                description: Password.
                example: secret
              date_of_birth:
                type: string
                format: date
                description: Date of birth.
                example: 1990-01-01
              phone_number:
                type: string
                description: Phone number.
                example: +123456789
              signed_in_provider:
                type: string
                description: Signed-in provider.
                example: google
    responses:
        200:
            description: OK, but User not created.
        201:
            description: User Created.
        400:
            description: All fields are required.
        500:
            description: Error creating new user
    """
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    picture = request.json.get("picture")
    password = request.json.get("password")
    date_of_birth = request.json.get("date_of_birth")
    phone_number = request.json.get("phone_number")
    signed_in_provider = request.json.get("signed_in_provider")

    if not (
        password
        and first_name
        and last_name
        and email
        and date_of_birth
        and phone_number
        and signed_in_provider
        and picture
    ):
        return jsonify({"message": "All fields are required."}), 400

    result = create_user(
        first_name,
        last_name,
        email,
        picture,
        password,
        date_of_birth,
        phone_number,
        signed_in_provider,
    )

    return jsonify(result), result["code"]


@users_blueprint.route("/logout/", methods=["POST", "GET"])
def logout_current_user():
    """
    Logout user
    ---
    tags:
      - Authentication
    consumes:
        - application/json
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            logout_all:
              type: boolean
              default: false
    responses:
        200:
            description: User successfully logged out
        401:
            description: User is not signed in
        500:
            description: An error occurred during logout
    """
    # API logout
    if request.is_json:
        response = jsonify({"msg": "logout successful"}), 200
        unset_jwt_cookies(response)
        return response

    # Session-based logout
    logout_user()
    session.pop("user_id", None)
    return redirect(url_for("users.login"))


@users_blueprint.route("/enable/", methods=["POST"])
@swag_from(
    {
        "tags": ["users"],
        "responses": {
            404: {"description": "User not found"},
            200: {"description": "User enabled successfully"},
            500: {"description": "An error occurred during enabling"},
        },
        "parameters": [
            {
                "name": "id",
                "in": "json",
                "required": True,
                "type": "integer",
                "description": "Id of the user",
            }
        ],
    }
)
def enable_user():
    user_id = request.json.get("id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    if user.enabled:
        return jsonify({"message": "User is already enabled."}), 200

    user.enabled = True
    user.save()
    return jsonify({"message": f"User {user.email} enabled successfully."}), 200


@users_blueprint.route("/disable/", methods=["POST"])
@swag_from(
    {
        "tags": ["users"],
        "responses": {
            404: {"description": "User not found"},
            200: {"description": "User disabled successfully"},
            500: {"description": "An error occurred during disabling"},
        },
        "parameters": [
            {
                "name": "id",
                "in": "json",
                "required": True,
                "type": "integer",
                "description": "Id of the user",
            }
        ],
    }
)
def disable_user():
    user_id = request.json.get("id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    if not user.enabled:
        return jsonify({"message": "User is already disabled."}), 200

    user.enabled = False
    user.save()
    return jsonify({"message": f"User {user.email} disabled successfully."}), 200


@users_blueprint.route("/delete/", methods=["DELETE"])
@swag_from(
    {
        "tags": ["users"],
        "responses": {
            404: {"description": "User not found"},
            200: {"description": "User deleted successfully"},
            500: {"description": "An error occurred during deletion"},
        },
        "parameters": [
            {
                "name": "id",
                "in": "query",
                "required": True,
                "type": "integer",
                "description": "Id of the user",
            }
        ],
    }
)
def delete_user():
    user_id = request.args.get("id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    try:
        user.delete()
        return jsonify({"message": f"User {user.email} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred during deletion."}), 500


@users_blueprint.route("/all/", methods=["GET"])
@swag_from(
    {
        "tags": ["users"],
        "responses": {
            200: {
                "description": "All users fetched successfully",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "_id": {"type": "string"},
                            "active": {"type": "boolean"},
                            "created_at": {"type": "string", "format": "date-time"},
                            "date_joined": {"type": "string", "format": "date-time"},
                            "date_of_birth": {"type": "string", "format": "date"},
                            "email": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "password": {"type": "string"},
                            "phone_number": {"type": "string"},
                            "picture": {"type": "string"},
                            "signed_in_provider": {"type": "string"},
                            "updated_at": {"type": "string", "format": "date-time"},
                        },
                    },
                },
            }
        },
    }
)
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200
