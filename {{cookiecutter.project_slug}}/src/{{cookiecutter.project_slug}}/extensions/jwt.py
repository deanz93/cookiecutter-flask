from flask_jwt_extended import JWTManager

class JWTToken:
    """
    A class for initializing and managing JWT tokens using Flask-JWT-Extended.

    Attributes:
        jwt (JWTManager): The JWTManager instance to handle JWT operations.
    """

    def __init__(self, app=None):
        """
        Initializes the JWTToken class.

        If an app instance is provided, it initializes Flask-JWT-Extended.

        Parameters:
            app (Flask, optional): The Flask application instance. Defaults to None.
        """
        self.jwt = None
        if app is not None:
            self.init_app(app)


    def init_app(self, app):
        """
        Initializes JWT using the provided Flask app instance.

        Parameters:
            app (Flask): The Flask application instance.
        """
        try:
            print("Initializing JWT...")
            self.jwt = JWTManager(app)
        except Exception as e:
            with app.app_context():
                app.logger.error(f"Error initializing JWT: {e}")
        finally:
            print("JWT initialized successfully.")
