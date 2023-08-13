from threading import Thread

from domain.model.StorageEvent import StorageEvent
from domain.repository.ClientLocalRepository import ClientLocalRepository
from domain.repository.RemoteFileStorageRepository import RemoteFileStorageRepository
from domain.repository.UserRepository import UserRepository


class MainControlViewModel:

    def __init__(
            self, user_repo: UserRepository, local_repo: ClientLocalRepository,
            file_storage_repo: RemoteFileStorageRepository
    ):
        self.__user_repo = user_repo
        self.__local_repo = local_repo
        self.__storage_repo = file_storage_repo
        self.__user = local_repo.get_main_user()

        Thread(
            target=lambda: self.__storage_repo.stream_storage_events(self.__user.user_id, self.process_event)
        ).start()

        self.downloads_set = set()

    def process_event(self, event, data):
        if event is StorageEvent.RealtimeDataPutEvent:
            if data['img'] not in self.downloads_set:
                print(data['img'], self.__local_repo.get_default_downloading_directory())
                self.__storage_repo.download_file(
                    data['img'], self.__local_repo.get_default_downloading_directory()
                )
                self.downloads_set.add(data['img'])

    def get_user(self):
        return self.__user

    def on_user_exit(self):
        self.__local_repo.clear_main_user()

    def on_download_directory_chosen(self, path):
        if path is not None:
            self.__local_repo.set_default_downloading_directory(path)

    def on_connection_retry_clicked(self):
        pass

    def on_connection_stop_clicked(self):
        pass
