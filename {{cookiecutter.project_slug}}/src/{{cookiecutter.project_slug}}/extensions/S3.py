
import boto3

from flask import current_app


class S3Storage(object):
    def __init__(self, app=None):
        self.s3_client = None
        self.bucket_name = None

        if app is not None:
            self.init_app(app)


    def init_app(self, app):
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


    def upload_file(self, file_path, s3_key):
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
        except Exception as e:
            current_app.logger.error(f"Failed to upload file to S3: {e}")
            return None

    def download_file(self, s3_key, download_path):
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, download_path)
            return download_path
        except Exception as e:
            current_app.logger.error(f"Failed to download file from S3: {e}")
            return None


    def delete_file(self, s3_key):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to delete file from S3: {e}")
            return False


    def list_objects(self, prefix='', delimiter='/'):
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