"""
This module provides an S3 storage class for interacting with Amazon S3.

Classes:
    S3Storage: A class for uploading, downloading, and managing files on S3.
"""
import boto3

from flask import current_app


class S3Storage(object):
    """
    A class for uploading, downloading, and managing files on Amazon S3.

    This class provides methods for interacting with Amazon S3, including
    uploading files, downloading files, and listing files in a bucket.

    Attributes:
        s3_client (boto3.client): The S3 client used to interact with Amazon S3.
        bucket_name (str): The name of the S3 bucket.

    Methods:
        __init__(app=None): Initializes a new instance of the S3Storage class.
        init_app(app): Initializes the S3 client using the application's configuration.
        upload_file(file_path, key): Uploads a file to Amazon S3.
        download_file(key, file_path): Downloads a file from Amazon S3.
        list_files(): Lists the files in the S3 bucket.
    """

    def __init__(self, app=None):
        """
        Initializes a new instance of the S3Storage class.

        This constructor optionally accepts a Flask application instance,
        which is used to initialize the S3 client immediately. If the app
        is provided, it calls the `init_app` method to set up the S3 client
        using the application's configuration.

        Args:
            app (Flask, optional): The Flask application instance to use
                for initializing the S3 client. Defaults to None.
        """

        self.s3_client = None
        self.bucket_name = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the S3 client.

        Args:
            app (Flask): The Flask application instance.

        Raises:
            ValueError: If the S3 configuration is not complete.
            Exception: If an error occurs while initializing the S3 client.

        Initializes the S3 client using the provided Flask app instance.
        It retrieves the S3 credentials from the instance's configuration,
        creates a boto3 S3 client, and sets up the S3 storage.
        If the S3 configuration is not complete, it raises a ValueError.
        If an error occurs while initializing the S3 client, it logs
        the error using the Flask app's logger.
        """
        try:
            print('Initializing S3 client...')
            if (not app.config.get('S3_REGION') or
                    not app.config.get('S3_ENDPOINT') or
                    not app.config.get('S3_ACCESS_KEY') or
                    not app.config.get('S3_SECRET_KEY')):
                raise ValueError("S3 configuration is not complete. Please check your .env file.")
            self.s3_client = boto3.client(
                's3',
                region_name=app.config.get('S3_REGION'),
                endpoint_url=app.config.get('S3_ENDPOINT'),
                aws_access_key_id=app.config.get('S3_ACCESS_KEY'),
                aws_secret_access_key=app.config.get('S3_SECRET_KEY'),
            )
            self.bucket_name = app.config.get('S3_BUCKET')
            app.extensions = getattr(app, 'extensions', {})
            app.extensions['s3_storage'] = self  # Register extension
        except Exception as e:
            with app.app_context():
                current_app.logger.error(f"\033[93mFailed to initialize S3 client. {e}\033[0m ")
        finally:
            print('S3 client initialized.')


    def upload_file(self, file_path, s3_key):
        """
        Uploads a file to the specified S3 bucket.

        Parameters:
            file_path (str): The path to the file to be uploaded.
            s3_key (str): The key to be used in S3.

        Returns:
            str: The S3 URL of the uploaded file, or None if the upload fails.

        Raises:
            Exception: If an error occurs while uploading the file to S3.

        Uploads the file at the specified path to the specified S3 bucket.
        If the upload is successful, it returns the S3 URL of the uploaded file.
        If the upload fails, it logs the error using the Flask app's logger
        and returns None.
        """
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
        except Exception as e:
            current_app.logger.error(f"Failed to upload file to S3: {e}")
            return None

    def download_file(self, s3_key, download_path):
        """
        Downloads a file from the specified S3 bucket.

        Parameters:
            s3_key (str): The key of the file to be downloaded from S3.
            download_path (str): The local path where the downloaded file will be saved.

        Returns:
            str: The local path where the file is downloaded, or None if the download fails.

        Raises:
            Exception: If an error occurs while downloading the file from S3.

        Attempts to download a file with the specified S3 key from the bucket
        and save it to the given local path. If the download is successful,
        it returns the local path. If the download fails, it logs the error
        using the Flask app's logger and returns None.
        """
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, download_path)
            return download_path
        except Exception as e:
            current_app.logger.error(f"Failed to download file from S3: {e}")
            return None

    def delete_file(self, s3_key):
        """
        Deletes a file from the specified S3 bucket.

        Parameters:
            s3_key (str): The key of the file to be deleted from S3.

        Returns:
            bool: True if the deletion is successful, False otherwise.

        Raises:
            Exception: If an error occurs while deleting the file from S3.

        Deletes a file with the specified S3 key from the bucket.
        If the deletion is successful, it returns True.
        If the deletion fails, it logs the error using the Flask app's logger
        and returns False.
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to delete file from S3: {e}")
            return False

    def list_objects(self, prefix='', delimiter='/'):
        """
        Lists objects in the specified S3 bucket.

        Parameters:
            prefix (str, optional): The prefix for filtering objects in the bucket. Defaults to ''.
            delimiter (str, optional): The delimiter for grouping objects. Defaults to '/'.

        Returns:
            dict: The response from the S3 service containing the list of objects if successful.
            list: An empty list if the request fails.

        Raises:
            Exception: If an error occurs while listing objects in the S3 bucket.

        Attempts to list objects in the specified S3 bucket with the given prefix and delimiter.
        If successful, it returns the response from the S3 service. If it fails, it logs the
        error using the Flask app's logger and returns an empty list.
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Delimiter=delimiter,
                Prefix=prefix
            )
            return response
        except Exception as e:
            current_app.logger.error(f"Failed to list objects in S3: {e}")
            return []
