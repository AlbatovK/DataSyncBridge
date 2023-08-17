from abc import ABCMeta, abstractmethod
from typing import Union


class RemoteFileStorageRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def stream_storage_events(self, user_id: Union[int, str], events_handler: callable):
        pass

    @abstractmethod
    def download_file(self, file_name, local_dir):
        pass

    @abstractmethod
    def list_remote_storage_files(self):
        pass

    @abstractmethod
    def stop_streaming(self):
        pass

    @abstractmethod
    def close_resources(self):
        pass
