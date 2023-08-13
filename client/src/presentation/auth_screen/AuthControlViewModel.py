from enum import Enum

import requests

from data.repository.ClientLocalRepositoryImpl import ClientLocalRepositoryImpl
from data.repository.RemoteFileStorageRepositoryImpl import RemoteFileStorageRepositoryImpl
from domain.repository.ClientLocalRepository import ClientLocalRepository
from domain.repository.UserRepository import UserRepository
from presentation.utility.LiveData import LiveData


class AuthControlViewModel:
    class AuthState(Enum):
        AuthStarted = 0
        AuthUserNotFoundError = 1
        AuthConnectionFailedError = 2
        AuthDataInvalid = 3
        AuthSuccess = 4

    def __init__(self, user_repo: UserRepository, local_repo: ClientLocalRepository):
        self.__user_repo = user_repo
        self.__local_repo = local_repo
        self.auth_state = LiveData()

    def on_data_submit(self, data):

        if not data.isdigit() or data is None:
            self.auth_state.data = AuthControlViewModel.AuthState.AuthDataInvalid
            return

        self.auth_state.data = AuthControlViewModel.AuthState.AuthStarted
        try:
            user_id = int(data)
            user = self.__user_repo.get_user_by_id(user_id)
        except requests.exceptions.ConnectionError:
            self.auth_state.data = AuthControlViewModel.AuthState.AuthConnectionFailedError
            return

        if user is None:
            self.auth_state.data = AuthControlViewModel.AuthState.AuthUserNotFoundError
            return

        self.__local_repo.set_main_user(user)
        self.auth_state.data = AuthControlViewModel.AuthState.AuthSuccess
