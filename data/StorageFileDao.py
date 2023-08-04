from pyrebase.pyrebase import Firebase


class StorageFileDao:

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()

    def get_user(self, user: dict):
        return self.__db.child('users').child(user['id']).get().val()

    def save_user(self, user: dict):
        self.__db.child('users').child(user['id']).set(
            {
                'name': user['name']
            }
        )

    def add_photo_to_user(self, user: dict, file_name: str):
        self.__db.child('users').child(user['id']).child('photo').push(
            {
                'img': file_name
            }
        )
