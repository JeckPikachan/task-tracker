from app.model.UniqueObject import UniqueObject


class TaskList(UniqueObject):
    """

    Task list used to group tasks
    Task lists exist in terms of project only
    """

    def __init__(self, **kwargs):
        name = kwargs.get('name')
        super(TaskList, self).__init__(name, kwargs.get('unique_id', None))
        self.tasks_list = kwargs.get('tasks_list', [])
