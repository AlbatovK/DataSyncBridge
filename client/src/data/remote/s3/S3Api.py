from os.path import join
from typing import List

from boto3.s3.transfer import TransferConfig
from botocore.client import BaseClient


class S3Api:

    def __init__(
            self,
            main_bucket: str,
            s3_client: BaseClient,
            config=TransferConfig(use_threads=False)
    ):
        self.__s3_client = s3_client
        self.__main_bucket = main_bucket
        self.__config = config

    def s3_upload_file(self, file_name: str):
        self.__s3_client.upload_file(file_name, self.__main_bucket, file_name, Config=self.__config)

    def s3_download_file(self, file_name: str, local_dir: str):
        self.__s3_client.download_file(self.__main_bucket, file_name, join(local_dir, file_name), Config=self.__config)

    def s3_list_objects(self) -> List:
        return self.__s3_client.list_objects(Bucket=self.__main_bucket).get('Contents', [])

    def s3_delete_file(self, file_name: str):
        self.__s3_client.delete_object(Bucket=self.__main_bucket, Key=file_name)
