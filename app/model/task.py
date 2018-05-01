from app.model.UniqueObject import UniqueObject
from app.util.enum_json import as_enum
from app.util.priority import Priority
from app.util.status import Status


class Task(UniqueObject):
    def __init__(self, **kwargs):
        unique_id = kwargs.get('unique_id', None)
        name = kwargs.get('name', None)
        super(Task, self).__init__(name, unique_id)

        self.description = kwargs.get('description', None)
        self.expiration_date = kwargs.get('expiration_date', None)
        self.priority = kwargs.get('priority', Priority.MIDDLE)
        self.status = kwargs.get('status', Status.CREATED)
        self.tags_list = kwargs.get('tags_list', [])
        self.comment_ids_list = kwargs.get('comment_ids_list', [])
        self.responsible_ids_list = kwargs.get('responsible_ids_list', [])
        self.author = kwargs.get('author', None)
        self.sub_tasks_list = kwargs.get('sub_tasks_list', [])

        if not isinstance(self.status, Status):
            self.status = as_enum(self.status)
        if not isinstance(self.priority, Priority):
            self.priority = as_enum(self.priority)

