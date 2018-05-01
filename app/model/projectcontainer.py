class ProjectContainer:
    def __init__(self, **kwargs):
        self.project = kwargs.get('project')
        self.lists = kwargs.get('lists', [])
        self.tasks = kwargs.get('tasks', [])

    def add_list(self, task_list):
        self.lists.append(task_list)
        self.project.lists.append(task_list.unique_id)

    def change_task_list_name(self, task_list_id, new_name):
        task_list = self._get_task_list_by_id(task_list_id)
        if task_list is not None:
            task_list.name = new_name

    def add_task(self, task_list_id, task):
        task_list = self._get_task_list_by_id(task_list_id)
        if task_list is not None:
            self.tasks.append(task)
            task_list.tasks_list.append(task.unique_id)

    def remove_task(self, task_id):
        for task_list in self.lists:
            task_list.tasks_list.remove(task_id)
        self.tasks = [task for task in self.tasks if task.unique_id != task_id]

    def free_tasks_list(self, task_list_id):
        task_list = self._get_task_list_by_id(task_list_id)
        self.tasks = [task for task in self.tasks if task.unique_id not in task_list.tasks_list]
        task_list.tasks_list.clear()

    def get_tasks(self, task_list_id=None):
        if task_list_id is None:
            return self.tasks
        else:
            task_list = self._get_task_list_by_id(task_list_id)
            if task_list is not None:
                return [task for task in self.tasks if task.unique_id in task_list.tasks_list]
            return None

    def _get_task_list_by_id(self, task_list_id):
        return next((x for x in self.lists if x.unique_id == task_list_id), None)
