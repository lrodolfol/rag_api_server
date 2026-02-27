import os

import boto3
from botocore.exceptions import ClientError

from static.LogginService import LoggerService
from static.Settings import Settings


class BucketClient:
    def __init__(self):
        self.s3 = None
        self.logger = LoggerService("RequestClient", "INFO")
        settings: Settings = Settings()

        self.host = settings.bucket("host")
        self.access_key = os.getenv("CLOUD_SECRET_KEY")
        self.secret_key = os.getenv("CLOUD_ACCESS_KEY")
        self.name = settings.bucket("name")
        self.region = settings.bucket("region")

        self.create_bucket_if_not_exists()

        self.s3 = boto3.client(
            "s3",
            endpoint_url=self.host,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )

        self.create_bucket_if_not_exists()

    def check_if_bucket_exists(self)  -> bool:
        try:
            self.s3.head_bucket(Bucket=self.name)
            return True
        except ClientError as e:
            return False

    def create_bucket_if_not_exists(self):
        if self.check_if_bucket_exists():
            return

        try:
            self.s3.create_bucket(Bucket=self.name)
        except ClientError as e:
            if not e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
                self.logger.error(f"Error creating bucket: {str(e)}")

    def upload_string_client_file(self, file: str, client_code: str):
        self.s3.put_object(
            Bucket=self.name,
            Key=client_code,
            Body=file.encode("utf-8"),
            ContentType="text/plain; charset=utf-8"
        )

    def read_client_file(self, client_code: str) -> str:
        try:
            response = self.s3.get_object(Bucket=self.name, Key=client_code)
            return response["Body"].read().decode("utf-8")
        except ClientError as e:
            self.logger.error(f"Error reading client file: {str(e)}")
            return ""

    def delete_file_client(self, client_code: str):
        try:
            self.s3.delete_object(Bucket=self.name, Key=client_code)
        except ClientError as e:
            self.logger.error(f"Error deleting client file: {str(e)}")
