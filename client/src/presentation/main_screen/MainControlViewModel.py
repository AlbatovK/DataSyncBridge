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

        self.start_stream_process()

        self.remote_storage_files_live_data = LiveData()
        self.active = True

        self.downloaded = set()

        Thread(target=self.async_reload).start()

    def close(self):
        self.active = False

    def start_stream_process(self):
        Thread(
            target=lambda: self.__storage_repo.stream_storage_events(self.__user.user_id, self.process_event)
        ).start()

    def process_event(self, event, data):

        if not self.active:
            return

        self.storage_event_live_data.data = event

        print(event, data)

        if data is None:
            return

        if event is StorageEvent.RealtimeDataPutEvent:

            if data['img'] in self.downloaded:
                return

            self.__storage_repo.download_file(
                data['img'], self.__local_repo.get_default_downloading_directory()
            )

            self.downloaded.add(
                data['img']
            )

        elif event is StorageEvent.OverdueDataPutEvent:

            directory_files = self.__local_repo.list_default_downloading_directory()

            remote_files = [
                (
                    x.file_name, join(self.__local_repo.get_default_downloading_directory(), x.file_name)
                ) for x in self.__storage_repo.list_remote_storage_files()
            ]

            for f_name, path in remote_files:
                if f_name not in directory_files and f_name not in self.downloaded:
                    print(f_name)

                    self.__storage_repo.download_file(
                        f_name, self.__local_repo.get_default_downloading_directory()
                    )

                    self.downloaded.add(f_name)

        Thread(target=self.async_reload).start()

    def async_reload(self):
        self.remote_storage_files_live_data.data = [
            join(self.__local_repo.get_default_downloading_directory(), x.file_name)
            for x in self.__storage_repo.list_remote_storage_files()
        ]

    def get_user(self):
        return self.__user

    def on_user_exit(self):
        self.__local_repo.clear_main_user()

    def on_download_directory_chosen(self, path):
        if path is not None:
            self.__local_repo.set_default_downloading_directory(path)
        self.__storage_repo.stop_streaming()
        self.start_stream_process()

    def on_connection_retry_clicked(self):
        self.start_stream_process()

    def on_connection_stop_clicked(self):
        self.__storage_repo.stop_streaming()
