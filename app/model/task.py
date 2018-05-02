from datetime import date, datetime

from app.model.UniqueObject import UniqueObject
from app.util.enum_json import as_enum
from app.util.priority import Priority
from app.util.status import Status


class Task(UniqueObject):
    def __init__(self, **kwargs):
        unique_id = kwargs.get('unique_id', None)
        name = kwargs.get('name', None)
        super(Task, self).__init__(name, unique_id)

        self._status = None
        self._priority = None
        self._expiration_date = None

        self.description = kwargs.get('description', None)
        self.expiration_date = kwargs.get('expiration_date', None)
        self.priority = kwargs.get('priority', Priority.MIDDLE)
        self.status = kwargs.get('status', Status.CREATED)
        self.tags_list = kwargs.get('tags_list', [])
        self.comment_ids_list = kwargs.get('comment_ids_list', [])
        self.responsible_ids_list = kwargs.get('responsible_ids_list', [])
        self.author = kwargs.get('author', None)
        self.sub_tasks_list = kwargs.get('sub_tasks_list', [])

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
        elif not isinstance(priority, Priority):
            self._priority = as_enum(priority)
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
        elif not isinstance(status, Status):
            self._status = as_enum(status)
        else:
            self._status = status
