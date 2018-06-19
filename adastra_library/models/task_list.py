from adastra_library.models.unique_object import UniqueObject


class TaskList(UniqueObject):
    """

    Task list used to group tasks
    Task lists exist in terms of project only
    """

    def __init__(self, name=None, unique_id=None, tasks_list=None):
        """

        :param name: {string} Name of task list
        :param unique_id: {string} Sets unique id of task list
                (use for restoring only)
        :param tasks_list: {string[]} A list of tasks unique ids
                (use for restoring only)
        """
        super(TaskList, self).__init__(name, unique_id)
        self.tasks_list = tasks_list if tasks_list is not None else []
