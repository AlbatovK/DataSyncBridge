from abc import ABCMeta, abstractmethod
from typing import Union

from domain.model.User import User


class UserRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_user_by_id(self, user_id: Union[int, str]) -> User:
        pass

    @abstractmethod
    def delete_user_file_node(self, user_id, node):
        pass
