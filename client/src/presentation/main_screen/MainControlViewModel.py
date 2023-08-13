from domain.repository.ClientLocalRepository import ClientLocalRepository
from domain.repository.UserRepository import UserRepository


class MainControlViewModel:

    def __init__(self, user_repo: UserRepository, local_repo: ClientLocalRepository):
        self.__user_repo = user_repo
        self.__local_repo = local_repo
        self.__user = local_repo.get_main_user()

    def get_user(self):
        return self.__user

    def on_user_exit(self):
        self.__local_repo.clear_main_user()

    def on_download_directory_chosen(self, e):
        print(e.__dict__)

    def on_connection_retry_clicked(self):
        pass

    def on_connection_stop_clicked(self):
        pass
