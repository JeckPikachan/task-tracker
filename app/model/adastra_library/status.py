from enum import Enum, auto


class Status(Enum):
    CREATED = auto()
    IN_WORK = auto()
    DONE = auto()

    @staticmethod
    def get_by_number(number):
        """

        :param number: {int} Number form 0 to 2 to be transformed
            into Status object
        :return: Status object or None
        """
        if number is None:
            return None
        if number == 0:
            return Status.CREATED
        if number == 1:
            return Status.IN_WORK
        if number == 2:
            return Status.DONE