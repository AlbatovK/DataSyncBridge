from abc import ABCMeta, abstractmethod

from domain.model.User import User


class ClientLocalRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_user_set(self):
        pass

    @abstractmethod
    def set_main_user(self, user: User):
        pass

    @abstractmethod
    def get_main_user(self):
        pass

    @abstractmethod
    def clear_main_user(self):
        pass
