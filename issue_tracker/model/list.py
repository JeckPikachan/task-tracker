from model.UniqueObject import UniqueObject


class List(UniqueObject):
    def __init__(self, name, **kwargs):
        super(List, self).__init__(name, kwargs.get('unique_id', None))
        self.tasks_list = kwargs.get('tasks_list', [])
