from enum import Enum


class StorageEvent(Enum):
    ConnectionSettledEvent = -1
    OverdueDataPutEvent = 0
    RealtimeDataPutEvent = 1
    ConnectionLostEvent = 2
    ConnectionStoppedEvent = 3
