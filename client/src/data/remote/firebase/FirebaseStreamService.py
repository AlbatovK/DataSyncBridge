from typing import Union

from pyrebase.pyrebase import Firebase

from domain.model.StorageEvent import StorageEvent


class FirebaseStreamService:
    __stream = None

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()

    def start_streaming(self, stream_user_id: Union[str, int], stream_event_handler: callable):
        def stream_handler(e):
            if e['path'] == "/":
                event = StorageEvent.OverdueDataPutEvent
                data = e['data']
            else:
                event = StorageEvent.RealtimeDataPutEvent
                data = e['data']
            stream_event_handler(event, data)

        stream_path = self.__db.child('users').child(stream_user_id).child('photo')
        self.__stream = stream_path.stream(stream_id='dsb_stream', stream_handler=stream_handler, is_async=True)
        self.__stream.start_stream()
