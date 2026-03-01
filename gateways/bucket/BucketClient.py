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

        self.host = settings.bucket["host"]
        self.access_key = os.getenv("CLOUD_ACCESS_KEY")
        self.secret_key = os.getenv("CLOUD_SECRET_KEY")
        self.name = settings.bucket["name"]
        self.region = settings.bucket["region"]

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


    def upload_string_client_file(self, file: str, key: str):
        self.s3.put_object(
            Bucket=self.name,
            Key=key,
            Body=file.encode("utf-8"),
            ContentType="text/plain; charset=utf-8"
        )


    def read_client_file(self, key: str) -> str:
        try:
            response = self.s3.get_object(Bucket=self.name, Key=key)
            return response["Body"].read().decode("utf-8")
        except ClientError as e:
            self.logger.error(f"Error reading client file: {str(e)}")
            return ""


    def read_big_file_services(self):
        pass


    # def append_file_client(self, file: str):
    #     existing_content = self.read_client_file('client_services.md')
    #     new_content = existing_content + file

    #     self.upload_string_client_file(new_content, 'services')


    def delete_file_client(self, key: str):
        try:
            self.s3.delete_object(Bucket=self.name, Key=key)
        except ClientError as e:
            self.logger.error(f"Error deleting client file: {str(e)}")


    def rename_file_client(self, old_key: str, new_key: str):
        try:
            copy_source = {'Bucket': self.name, 'Key': old_key}
            self.s3.copy_object(CopySource=copy_source, Bucket=self.name, Key=new_key)
            self.delete_file_client(old_key)
        except ClientError as e:
            self.logger.error(f"Error renaming client file: {str(e)}")