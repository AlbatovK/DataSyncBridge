from abc import ABCMeta, abstractmethod


class AbstractModule:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def inject_dependencies(cls, firebase_config, s3_config, local_storage, on_fall_back):
        pass
