from .UniqueObject import UniqueObject


class TaskList(UniqueObject):
    """

    Task list used to group tasks
    Task lists exist in terms of project only
    """

    def __init__(self, **kwargs):
        """

        :param kwargs: can include
            name: {string} Name of task list
            unique_id: {string} Sets unique id of task list
                (use for restoring only)
            tasks_list: {string[]} A list of tasks unique ids
                (use for restoring only)
        """
        name = kwargs.get('name')
        super(TaskList, self).__init__(name, kwargs.get('unique_id', None))
        self.tasks_list = kwargs.get('tasks_list', [])
