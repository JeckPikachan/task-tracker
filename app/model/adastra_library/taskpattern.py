import copy


class TaskPattern:
    """

    TaskPattern class is used to create task patterns
    for further planning and creating tasks based on it
    """
    def __init__(self,
                 name,
                 description=None,
                 priority=None,
                 status=None,
                 author=None):
        """

        :param name: {string} Name of task to be created
        :param description: {string} Description of task to be created
        :param priority: {int} Priority of task to be created
        :param status: {int} Status of task to be created
        :param author: {string} Author id of task to be created
        """
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.author = author

    def get_task_create_params(self):
        return copy.deepcopy(self.__dict__)
