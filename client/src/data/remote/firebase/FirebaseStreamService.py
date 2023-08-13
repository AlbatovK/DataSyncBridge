from typing import Union

from pyrebase.pyrebase import Firebase


class FirebaseStreamService:
    __stream = None

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()

    def start_streaming(self, stream_user_id: Union[str, int], callback_handler: callable):
        stream_path = self.__db.child('users').child(stream_user_id).child('photo')
        self.__stream = stream_path(stream_id='dsb_stream', callback_handler=callback_handler)
        self.__stream.start_stream()
