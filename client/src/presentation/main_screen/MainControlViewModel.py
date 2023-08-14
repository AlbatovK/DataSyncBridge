import os
import time
from os.path import join
from threading import Thread

from domain.model.StorageEvent import StorageEvent
from domain.repository.ClientLocalRepository import ClientLocalRepository
from domain.repository.RemoteFileStorageRepository import RemoteFileStorageRepository
from domain.repository.UserRepository import UserRepository
from presentation.utility.LiveData import LiveData


class MainControlViewModel:

    def __init__(
            self, user_repo: UserRepository, local_repo: ClientLocalRepository,
            file_storage_repo: RemoteFileStorageRepository
    ):
        self.__user_repo = user_repo
        self.__local_repo = local_repo
        self.__storage_repo = file_storage_repo
        self.__user = local_repo.get_main_user()

        self.storage_event_live_data = LiveData()
        self.downloads_set = set()

        self.start_stream_process()

        self.remote_storage_files_live_data = LiveData(
            self.__storage_repo.list_remote_storage_files()
        )

    def start_stream_process(self):
        Thread(
            target=lambda: self.__storage_repo.stream_storage_events(self.__user.user_id, self.process_event)
        ).start()

    def process_event(self, event, data):
        print(event)
        self.storage_event_live_data.data = event
        if event is StorageEvent.RealtimeDataPutEvent:
            if data['img'] not in self.downloads_set:
                self.__storage_repo.download_file(
                    data['img'], self.__local_repo.get_default_downloading_directory()
                )
                self.downloads_set.add(data['img'])
        elif event is StorageEvent.OverdueDataPutEvent:
            for _, file_dct in data.items():
                file = file_dct['img']
                if (file not in self.__local_repo.list_default_downloading_directory()
                        and file not in self.downloads_set):
                    self.downloads_set.add(file)
                    self.__storage_repo.download_file(
                        file, self.__local_repo.get_default_downloading_directory()
                    )

        def async_load():
            time.sleep(2)
            self.remote_storage_files_live_data.data = [
                join(self.__local_repo.get_default_downloading_directory(), x.file_name)
                for x in self.__storage_repo.list_remote_storage_files()
            ]

        Thread(target=async_load).start()

    def get_user(self):
        return self.__user

    def on_user_exit(self):
        self.__local_repo.clear_main_user()

    def on_download_directory_chosen(self, path):
        if path is not None:
            self.__local_repo.set_default_downloading_directory(path)

    def on_connection_retry_clicked(self):
        self.start_stream_process()

    def on_connection_stop_clicked(self):
        self.__storage_repo.close_resources()
