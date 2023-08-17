from enum import Enum


class StorageEvent(Enum):
    ConnectionSettledEvent = 0
    OverdueDataPutEvent = 1
    RealtimeDataPutEvent = 2
    ConnectionLostEvent = 3
    ConnectionStoppedEvent = 4
