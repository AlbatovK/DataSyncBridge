from flet_core.client_storage import ClientStorage


class LocalStorageApi:

    def __init__(self, client_storage: ClientStorage):
        self.__storage = client_storage

    def contains_key(self, key: str):
        return self.__storage.contains_key(key)

    def set(self, key: str, user_dto: dict):
        self.__storage.set(key, user_dto)

    def get(self, key: str):
        return self.__storage.get(key)

    def remove(self, key: str):
        self.__storage.remove(key)

    def clear(self):
        self.__storage.clear()
