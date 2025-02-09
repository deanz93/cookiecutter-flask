from flask import request, Response
from functools import wraps

from modules.users.models import User


def requires_basic_auth(f):
    """Decorator to require HTTP Basic Auth for your endpoint."""

    def check_auth(email, password):
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            return True
        return False

    def authenticate():
        return Response(
            "Authentication required.", 401,
            {"WWW-Authenticate": "Basic realm='Login Required'"},
        )

    @wraps(f)
    def decorated(*args, **kwargs):
        # NOTE: This example will require Basic Auth only when you run the
        # app directly. For unit tests, we can't block it from getting the
        # Swagger specs so we just allow it to go thru without auth.
        # The following two lines of code wouldn't be needed in a normal
        # production environment.
        if __name__ != "__main__":
            return f(*args, **kwargs)

        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def requires_bearer_auth(f):
    """Decorator to require HTTP Bearer Auth for your endpoint."""

    def authenticate():
        return Response(
            "Bearer token required.", 401,
            {"WWW-Authenticate": "Bearer realm='Bearer Token Required'"}
        )

    @wraps(f)
    def decorated(*args, **kwargs):
        # Allow Swagger to access the endpoint without Bearer Auth
        if request.path.startswith('/apidocs') or request.path.startswith('/swagger'):
            return f(*args, **kwargs)

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return authenticate()

        bearer_token = auth_header.split(' ')[1]
        # Add your logic here to verify the bearer token
        if not bearer_token:
            return authenticate()

        return f(*args, **kwargs)

    return decorated
