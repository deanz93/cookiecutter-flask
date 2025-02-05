"""
Contains the Firebase class.

This class provides methods to interact with the Firebase Admin SDK.

"""
from firebase_admin import credentials, initialize_app, firestore



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

    def __init__(self, app):
        """
        Initializes a new instance of the Firebase class.

        Sets up the Firebase credentials, initializes the Firebase app,
        and creates a Firestore client.

        Parameters:
            None

        Returns:
            None
        """
        self.creds = credentials.Certificate(app.config.get('GOOGLE_CREDENTIALS_FILEPATH'))
        self.app = initialize_app(self.creds)
        self.db = firestore.client()
