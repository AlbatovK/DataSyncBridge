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

        self.__user = local_repo.get_default_local_user()

        self.storage_event_live_data = LiveData()

        self.remote_storage_files_live_data = LiveData()

        self.active = True

        self.start_stream_process()

    def close(self):
        self.active = False
        self.__storage_repo.stop_streaming()

    def start_stream_process(self):
        Thread(
            target=lambda: self.__storage_repo.stream_storage_events(self.__user.user_id, self.process_event)
        ).start()

    def process_event(self, event, data):

        if not self.active:
            return

        self.storage_event_live_data.data = event

        print(event, data)

        if event is StorageEvent.RealtimeDataPutEvent:
            if data['data'] is None:
                return
            node, f_name = data['path'], data['data']['img']

            self.__storage_repo.download_file(
                f_name, self.__local_repo.get_default_downloading_directory()
            )

            self.__user_repo.delete_user_file_node(
                self.__user.user_id, node,
            )

        elif event is StorageEvent.OverdueDataPutEvent:

            if data is None:
                return

            for key, f_name in data.items():
                self.__storage_repo.download_file(
                    f_name['img'], self.__local_repo.get_default_downloading_directory()
                )

                self.__user_repo.delete_user_file_node(
                    self.__user.user_id, key
                )

        Thread(target=self.sync_downloaded_files).start()

    def get_user(self):
        return self.__user

    def on_user_exit(self):
        self.__local_repo.clear_default_local_user()

    def on_download_directory_chosen(self, path):
        if path is not None and path != self.__local_repo.get_default_downloading_directory():
            self.__local_repo.set_default_downloading_directory(path)
            self.sync_downloaded_files()

    def on_connection_retry_clicked(self):
        self.start_stream_process()

    def on_connection_stop_clicked(self):
        self.__storage_repo.stop_streaming()

    def sync_downloaded_files(self):
        self.remote_storage_files_live_data.data = [
            join(self.__local_repo.get_default_downloading_directory(), x) for x in
            self.__local_repo.list_default_downloading_directory()
        ]

    def on_mount(self):
        self.sync_downloaded_files()
