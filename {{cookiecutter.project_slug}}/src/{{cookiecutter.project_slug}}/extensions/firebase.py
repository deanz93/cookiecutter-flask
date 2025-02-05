"""
Contains the Firebase class.

This class provides methods to interact with the Firebase Admin SDK.

"""
import os
from firebase_admin import credentials, initialize_app, firestore

from flask import current_app


class Firebase(object):
    """
    Class to manage Firebase admin tasks.

    This class provides methods to interact with the Firebase Admin SDK.

    Attributes:
        creds (credentials.Certificate): The credentials to use
        when interacting with the Firebase Admin SDK.
        app (firebase_admin.App): The initialized Firebase app.
        db (firestore.Client): The Firestore client.

    Methods:
        __init__: Initializes the Firebase instance.
    """

    def __init__(self, app=None):
        """
        Initializes a new instance of the Firebase class.

        Sets up the Firebase credentials, initializes the Firebase app,
        and creates a Firestore client.

        Parameters:
            None

        Returns:
            None
        """
        self.creds = None
        self.app = None
        self.db = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the Firebase app.

        Parameters:
            app (Flask): The Flask application instance.

        Returns:
            None

        Raises:
            FileNotFoundError: If the credentials file is not found.
            Exception: If an error occurs while initializing the Firebase client.

        Initializes the Firebase app using the provided Flask app instance.
        It retrieves the Google credentials from the instance's configuration,
        creates a Firestore client, and sets up the Firebase app.
        If the credentials file is not found, it raises a FileNotFoundError.
        If an error occurs while initializing the Firebase client, it logs
        the error using the Flask app's logger.
        """
        try:
            print('Initializing Firebase...')
            if not os.path.isfile(app.config.get('GOOGLE_CREDENTIALS_FILEPATH')):
                raise FileNotFoundError(f"File {app.config.get('GOOGLE_CREDENTIALS_FILEPATH')} not found.")
            self.creds = credentials.Certificate(app.config.get('GOOGLE_CREDENTIALS_FILEPATH'))
            self.app = initialize_app(self.creds)
            self.db = firestore.client()
        except Exception as e:
            with app.app_context():
                current_app.logger.error(f"\033[93mFailed to initialize Firebase client.{e}\033[0m ")
