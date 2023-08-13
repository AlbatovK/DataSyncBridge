from data.local.LocalStorageApi import LocalStorageApi
from domain.model.User import User


class ClientLocalRepositoryImpl:
    __storage_api = None
    __instance = None

    @classmethod
    def initialize(cls, storage_api: LocalStorageApi):
        cls.__storage_api = storage_api

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = ClientLocalRepositoryImpl()
        return cls.__instance

    def is_user_set(self):
        return self.__storage_api.contains_key('user')

    def set_main_user(self, user: User):
        return self.__storage_api.set(
            'user',
            user.to_dto()
        )

    def get_main_user(self):
        return User.from_dto(
            self.__storage_api.get('user')
        ) if self.is_user_set() else None

    def clear_main_user(self):
        self.__storage_api.remove('user')
