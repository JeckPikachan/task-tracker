from enum import Enum, auto


class Status(Enum):
    CREATED = auto()
    IN_WORK = auto()
    DONE = auto()
