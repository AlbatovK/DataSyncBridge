from abc import ABCMeta, abstractmethod

from domain.model.User import User


class ClientLocalRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_user_set(self):
        pass

    @abstractmethod
    def set_default_downloading_directory(self, path):
        pass

    @abstractmethod
    def get_default_downloading_directory(self):
        pass

    @abstractmethod
    def set_main_user(self, user: User):
        pass

    @abstractmethod
    def get_main_user(self) -> User:
        pass

    @abstractmethod
    def clear_main_user(self):
        pass
