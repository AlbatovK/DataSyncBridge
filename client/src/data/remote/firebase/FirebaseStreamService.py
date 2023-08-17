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

    def strictly_close_stream(self):
        while True:
            try:
                self.__stream.close()
            except AttributeError:
                break

    def close_stream(self):
        self.__stream.stream_handler = lambda _: None
        self.strictly_close_stream()
        self.__stream = None

    def stop_streaming(self):
        self.__stream.stream_handler = lambda _: None

        self.strictly_close_stream()

        self.__stream_event_handler(
            StorageEvent.ConnectionStoppedEvent, None
        )

    def start_streaming(self, stream_user_id: Union[str, int], stream_event_handler: callable):

        self.__stream_event_handler = stream_event_handler
        self.__stream_event_handler(
            StorageEvent.ConnectionSettledEvent, None
        )

        def stream_handler(e):

            if e['event'] != 'put':
                return

            if e['path'] == "/":
                event = StorageEvent.OverdueDataPutEvent
                data = e['data']
            else:
                event = StorageEvent.RealtimeDataPutEvent
                data = e

            if self.__stream is not None and self.__last_event != e:
                self.__last_event = e
                self.__stream_event_handler(event, data)

        try:
            stream_path = self.__db.child('users').child(stream_user_id).child('photo')
            self.__stream = stream_path.stream(stream_id='dsb_stream', stream_handler=stream_handler, is_async=True)
            self.__stream.start_stream()
        except (requests.exceptions.ConnectionError, urllib3.exceptions.NewConnectionError):
            self.__stream_event_handler(
                StorageEvent.ConnectionLostEvent, None
            )
