from enum import Enum, auto


class Priority(Enum):
    LOW = auto()
    MIDDLE = auto()
    HIGH = auto()

    @staticmethod
    def get_by_number(number):
        if number is None:
            return None
        if number == 0:
            return Priority.LOW
        if number == 1:
            return Priority.MIDDLE
        if number == 2:
            return Priority.HIGH