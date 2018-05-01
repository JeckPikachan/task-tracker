from model.UniqueObject import UniqueObject


class TaskList(UniqueObject):
    def __init__(self, **kwargs):
        name = kwargs.get('name')
        super(TaskList, self).__init__(name, kwargs.get('unique_id', None))
        self.tasks_list = kwargs.get('tasks_list', [])
