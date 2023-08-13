from data.remote.firebase.FirebaseStreamService import FirebaseStreamService
from data.remote.s3.S3Api import S3Api
from domain.repository.RemoteFileStorageRepository import RemoteFileStorageRepository


class RemoteFileStorageRepositoryImpl(RemoteFileStorageRepository):
    __instance = None
    __stream_service: FirebaseStreamService = None
    __s3_api: S3Api

    @classmethod
    def initialize(
            cls,
            stream_service: FirebaseStreamService,
            s3_api: S3Api
    ):
        cls.__stream_service = stream_service
        cls.__s3_api = s3_api

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = RemoteFileStorageRepositoryImpl()
        return cls.__instance
