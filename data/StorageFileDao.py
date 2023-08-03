from pyrebase.pyrebase import Firebase


class StorageFileDao:

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()
