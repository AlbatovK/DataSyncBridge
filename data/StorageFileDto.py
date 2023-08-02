from pyrebase.pyrebase import Firebase


class StorageFileDto:

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()
