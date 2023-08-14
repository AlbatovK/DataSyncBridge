class Observer:

    def __init__(self, callback: callable):
        self.__callback = callback

    @property
    def callback(self):
        return self.__callback

    @callback.getter
    def callback(self) -> callable:
        return self.__callback
