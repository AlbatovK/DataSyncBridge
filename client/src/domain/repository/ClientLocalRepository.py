from abc import ABCMeta, abstractmethod

from domain.model.User import User


class ClientLocalRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_default_local_user_set(self):
        pass

    @abstractmethod
    def set_default_downloading_directory(self, path):
        pass

    @abstractmethod
    def delete_internal_file(self, path):
        pass

    @abstractmethod
    def get_default_downloading_directory(self):
        pass

    @abstractmethod
    def list_default_downloading_directory(self):
        pass

    @abstractmethod
    def set_default_local_user(self, user: User):
        pass

    @abstractmethod
    def get_default_local_user(self) -> User:
        pass

    @abstractmethod
    def clear_default_local_user(self):
        pass
