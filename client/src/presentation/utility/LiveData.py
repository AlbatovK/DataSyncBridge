from typing import Any


class LiveData:

    def __init__(self, data=None):
        self.__data = data
        self.__observers = []

    @property
    def data(self):
        return self.__data

    @data.getter
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: Any):
        self.__data = data
        for observer in self.__observers:
            observer.callback(data)

    @property
    def observers(self):
        return self.__observers

    @observers.getter
    def observers(self):
        return self.__observers

    def add_observer(self, observer):
        self.__observers.append(observer)
