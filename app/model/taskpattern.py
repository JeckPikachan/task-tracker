import copy


class TaskPattern:
    def __init__(self, name, description, priority, status, author):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.author = author

    def get_task_create_params(self):
        return copy.deepcopy(self.__dict__)
