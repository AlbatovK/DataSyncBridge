from typing import Union

import requests
import urllib3
from pyrebase.pyrebase import Firebase

from domain.model.StorageEvent import StorageEvent


class FirebaseStreamService:
    __stream = None
    __stream_event_handler = None
    __last_event = None

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()

    def close_stream(self):
        self.close_connection()
        self.__stream = None

    def close_connection(self):
        try:
            self.__stream.close()
        except AttributeError as e:
            print(e)

    def stop_streaming(self):
        self.__stream.stream_handler = lambda _: None

        self.__stream.close()
        self.__stream_event_handler(
            StorageEvent.ConnectionStoppedEvent, None
        )

    def start_streaming(self, stream_user_id: Union[str, int], stream_event_handler: callable):

        self.__stream_event_handler = stream_event_handler

        def stream_handler(e):
            print(e)
            if e['path'] == "/":
                event = StorageEvent.OverdueDataPutEvent
                data = e['data']
            else:
                event = StorageEvent.RealtimeDataPutEvent
                data = e['data']
            if self.__stream is not None:
                self.__last_event = e
                self.__stream_event_handler(event, data)
                self.__retried = False

        try:
            stream_path = self.__db.child('users').child(stream_user_id).child('photo')
            self.__stream = stream_path.stream(stream_id='dsb_stream', stream_handler=stream_handler, is_async=True)
            self.__stream.start_stream()
        except (requests.exceptions.ConnectionError, urllib3.exceptions.NewConnectionError):
            self.__stream_event_handler(
                StorageEvent.ConnectionLostEvent, None
            )
