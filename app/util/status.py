from enum import Enum, auto


class Status(Enum):
    CREATED = auto()
    IN_WORK = auto()
    DONE = auto()

    @staticmethod
    def get_by_number(number):
        if number is None:
            return None
        if number == 0:
            return Status.CREATED
        if number == 1:
            return Status.IN_WORK
        if number == 2:
            return Status.DONE
