from pyrebase.pyrebase import Firebase


class StorageFileDao:

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()

    def get_user(self, user: dict):
        data = self.__db.child('users').child(user['id']).get()
        return data

    def create_new_profile(self, user: dict):
        self.__db.child('users').child(user['id']).set({'name': user['name']})

    def add_photo(self, user: dict, file_name: str):
        self.__db.child('users').child(user['id']).child('photo').push({'img': file_name})