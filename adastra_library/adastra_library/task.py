from datetime import datetime
from enum import Enum

from adastra_library.adastra_library.unique_object import UniqueObject


class TaskRelation:
    def __init__(self, to, description=None):
        self.to = to
        self.description = description


class Status(Enum):
    CREATED = 0
    IN_WORK = 1
    DONE = 2

    @staticmethod
    def get_by_number(number):
        """

        :param number: {int} Number form 0 to 2 to be transformed
            into Status object
        :return: Status object or None
        """
        return Status(number)


class Priority(Enum):
    LOW = 0
    MIDDLE = 1
    HIGH = 2

    @staticmethod
    def get_by_number(number):
        """

        :param number: {int} Number form 0 to 2 to be transformed
            into Priority object
        :return: Priority object or None
        """
        return Priority(number)


class Task(UniqueObject):
    """

    Task is the most basic element of Task Tracker
    Tasks are grouped into Task Lists (TaskList)
    Tasks exist in terms of task lists only
    """
    def __init__(self,
                 name=None,
                 unique_id=None,
                 description=None,
                 expiration_date=None,
                 priority=None,
                 status=None,
                 author=None,
                 tags_list=None,
                 comment_ids_list=None,
                 responsible_ids_list=None,
                 related_tasks_list=None):
        """

        :param name: {string} Name of task
        :param unique_id: {string} Sets unique id of task
                (use for restoring only )
        :param description: {string} Description of task
        :param expiration_date: {date} A date when task expires
        :param priority: {Priority} task priority
        :param status: {Status} task status
        :param author: {string} author id
        :param tags_list: not implemented
        :param comment_ids_list: not implemented
        :param responsible_ids_list: not implemented
        :param related_tasks_list: not implemented
        """
        unique_id = unique_id
        name = name
        super(Task, self).__init__(name, unique_id)

        self._status = None
        self._priority = None
        self._expiration_date = None

        self.description = description
        self.expiration_date = expiration_date
        self.priority = priority if priority is not None else Priority.MIDDLE
        self.status = status if status is not None else Status.CREATED
        self.tags_list = tags_list if tags_list is not None else []
        self.comment_ids_list = (comment_ids_list if
                                 comment_ids_list is not None else [])
        self.responsible_ids_list = (responsible_ids_list if
                                     responsible_ids_list is not None else [])
        self.author = author
        self.related_tasks_list = ([TaskRelation(**x) for x in related_tasks_list] if
                                   related_tasks_list is not None else [])

    @property
    def expiration_date(self):
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, expiration_date):
        if isinstance(expiration_date, datetime):
            self._expiration_date = expiration_date
        elif isinstance(expiration_date, str):
            self._expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d %H:%M')
        else:
            self._expiration_date = None

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        if priority is None:
            self._priority = Priority.MIDDLE
        elif isinstance(priority, int):
            self._priority = Priority.get_by_number(priority)
        else:
            self._priority = priority

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status is None:
            self._status = Status.CREATED
        elif isinstance(status, int):
            self._status = Status.get_by_number(status)
        else:
            self._status = status

    def add_relation(self, to_id, description=None):
        """

        :param to_id: {string} id of task on which relation will be set
        :param description: {string} should describe task relation
        :return: {TaskRelation} An object of created task relation
        """
        task_relation = TaskRelation(to_id, description)
        self.related_tasks_list.append(task_relation)
        return task_relation

    def remove_relation(self, to_id):
        self.related_tasks_list = [x for x in
                                   self.related_tasks_list if
                                   x.to != to_id]
