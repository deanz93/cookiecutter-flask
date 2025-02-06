"""
Module with endpoints for user authentication

Endpoints:

    - /signin: Sign in and return a JWT token.

Imports:

    - flask: A web framework for Python.
    - flasgger: A library for generating Swagger documentation.
"""
from flasgger import swag_from
from flask import Blueprint, request, jsonify
from modules.users.models import User


users_blueprint = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')


@users_blueprint.route('/signin/', methods=['POST'])
@swag_from({
    'tags': ['users'],
    'responses': {
        200: {
            'description': 'Sign in successful'
        },
        401: {
            'description': 'Invalid username or password or user is disabled'
        }
    },
    'parameters': [
        {
            'name': 'username',
            'in': 'json',
            'required': True,
            'type': 'string',
            'description': 'Username of the user'
        },
        {
            'name': 'password',
            'in': 'json',
            'required': True,
            'type': 'string',
            'description': 'Password of the user'
        }
    ]
})
def signin():
    """
    Sign in with a username and password.

    Args:
        username (str): Username of the user.
        password (str): Password of the user.

    Returns:
        dict: A dict with a message indicating whether the sign in was successful or not.

    Raises:
        401: If the username or password is invalid or the user is disabled.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Check if the user is enabled
        if user.enabled:
            return jsonify({"message": f"User {username} signed in successfully."}), 200
        else:
            return jsonify({"message": "User is disabled."}), 401
    else:
        return jsonify({"message": "Invalid username or password."}), 401


@users_blueprint.route('/register/', methods=['POST'])
@swag_from({
    'tags': ['users'],
    'responses': {
        201: {
            'description': 'User registered successfully'
        },
        400: {
            'description': 'Username and password are required'
        },
        500: {
            'description': 'An error occurred during registration'
        }
    },
    'parameters': [
        {
            'name': 'username',
            'in': 'json',
            'required': True,
            'type': 'string',
            'description': 'Username of the user'
        },
        {
            'name': 'password',
            'in': 'json',
            'required': True,
            'type': 'string',
            'description': 'Password of the user'
        }
    ]
})
def register_user():
    """
    Register a new user.

    Args:
        username (str): Username of the user.
        password (str): Password of the user.

    Returns:
        dict: A dict with a message indicating whether the registration was successful or not.

    Raises:
        400: If the username and password are not provided.
        500: If an error occurred during registration.
    """
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    user = User(username=username, password=password)

    try:
        user.save()
        return jsonify({"message": f"User {username} registered successfully."}), 201
    except Exception as e:
        return jsonify({"message": "An error occurred during registration."}), 500


@users_blueprint.route('/enable/', methods=['POST'])
@swag_from({
    'tags': ['users'],
    'responses': {
        404: {
            'description': 'User not found'
        },
        200: {
            'description': 'User enabled successfully'
        },
        500: {
            'description': 'An error occurred during enabling'
        }
    },
    'parameters': [
        {
            'name': 'id',
            'in': 'json',
            'required': True,
            'type': 'integer',
            'description': 'Id of the user'
        }
    ]
})
def enable_user():
    """
    Enable a user.

    Args:
        id (int): Id of the user to be enabled.

    Returns:
        dict: A dict with a message indicating whether the user was enabled successfully or not.

    Raises:
        404: If the user is not found.
        200: If the user is already enabled.
        500: If an error occurred during enabling.
    """
    user_id = request.json.get('id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    if user.enabled:
        return jsonify({"message": "User is already enabled."}), 200

    user.enabled = True
    user.save()
    return jsonify({"message": f"User {user.email} enabled successfully."}), 200


@users_blueprint.route('/disable/', methods=['POST'])
@swag_from({
    'tags': ['users'],
    'responses': {
        404: {
            'description': 'User not found'
        },
        200: {
            'description': 'User disabled successfully'
        },
        500: {
            'description': 'An error occurred during disabling'
        }
    },
    'parameters': [
        {
            'name': 'id',
            'in': 'json',
            'required': True,
            'type': 'integer',
            'description': 'Id of the user'
        }
    ]
})
def disable_user():
    """
    Disable a user.

    Args:
        id (int): Id of the user to be disabled.

    Returns:
        dict: A dict with a message indicating whether the user was disabled successfully or not.

    Raises:
        404: If the user is not found.
        200: If the user is already disabled.
        500: If an error occurred during disabling.
    """
    user_id = request.json.get('id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    if not user.enabled:
        return jsonify({"message": "User is already disabled."}), 200

    user.enabled = False
    user.save()
    return jsonify({"message": f"User {user.email} disabled successfully."}), 200


@users_blueprint.route('/delete/', methods=['DELETE'])
@swag_from({
    'tags': ['users'],
    'responses': {
        404: {
            'description': 'User not found'
        },
        200: {
            'description': 'User deleted successfully'
        },
        500: {
            'description': 'An error occurred during deletion'
        }
    },
    'parameters': [
        {
            'name': 'id',
            'in': 'query',
            'required': True,
            'type': 'integer',
            'description': 'Id of the user'
        }
    ]
})
def delete_user():
    """
    Delete a user.

    Args:
        id (int): Id of the user to be deleted, passed as a query parameter.

    Returns:
        dict: A dict with a message indicating whether the user was deleted successfully or not.

    Raises:
        404: If the user is not found.
        200: If the user is deleted successfully.
        500: If an error occurred during deletion.
    """

    user_id = request.args.get('id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    try:
        user.delete()
        return jsonify({"message": f"User {user.email} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred during deletion."}), 500


@users_blueprint.route('/all/', methods=['GET'])
@swag_from({
    'tags': ['users'],
    'responses': {
        200: {
            'description': 'All users fetched successfully',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        '_id': {'type': 'string'},
                        'active': {'type': 'boolean'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        'date_joined': {'type': 'string', 'format': 'date-time'},
                        'date_of_birth': {'type': 'string', 'format': 'date'},
                        'email': {'type': 'string'},
                        'first_name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'password': {'type': 'string'},
                        'phone_number': {'type': 'string'},
                        'picture': {'type': 'string'},
                        'signed_in_provider': {'type': 'string'},
                        'updated_at': {'type': 'string', 'format': 'date-time'}
                    }}
            }
        }
    }
})
def get_all_users():
    """
    Get all users.

    Returns:
        list: A list of all users with their fields as a dict.

    Example response:
        [
            {
                "_id": "5f5f2a1a1a1a1a1a1a1a",
                "active": true,
                "created_at": "2020-09-15T14:30:00.000Z",
                "date_joined": "2020-09-15T14:30:00.000Z",
                "date_of_birth": "1990-01-01",
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "hashedpassword",
                "phone_number": "+1234567890",
                "picture": "https://example.com/picture.jpg",
                "signed_in_provider": "google",
                "updated_at": "2020-09-15T14:30:00.000Z"
            }
        ]
    """
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200
