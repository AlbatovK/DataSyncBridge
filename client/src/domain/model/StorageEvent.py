from enum import Enum


class StorageEvent(Enum):
    OverdueDataPutEvent = 0
    RealtimeDataPutEvent = 1
