from typing import Union

from data.remote.firebase.FirebaseStreamService import FirebaseStreamService
from data.remote.s3.S3Api import S3Api
from domain.model.RemoteStorageFile import RemoteStorageFile
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

    def list_remote_storage_files(self):
        return [RemoteStorageFile.from_dto(item) for item in self.__s3_api.s3_list_objects()]

    def stream_storage_events(self, user_id: Union[int, str], events_handler: callable):
        self.__stream_service.start_streaming(user_id, events_handler)

    def download_file(self, file_name, local_dir: str):
        self.__s3_api.s3_download_file(file_name, local_dir)

    def close_resources(self):
        self.__stream_service.stop_streaming()
