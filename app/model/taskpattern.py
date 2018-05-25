import copy


class TaskPattern:
    """

    TaskPattern class is used to create task patterns
    for further planning and creating tasks based on it
    """
    def __init__(self, name, description, priority, status, author):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.author = author

    def get_task_create_params(self):
        return copy.deepcopy(self.__dict__)
