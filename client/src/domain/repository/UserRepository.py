from abc import ABCMeta, abstractmethod
from typing import Union


class UserRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_user_by_id(self, user_id: Union[int, str]):
        raise NotImplementedError
