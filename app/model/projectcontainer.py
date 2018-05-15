class ProjectContainer:
    def __init__(self, **kwargs):
        self.project = kwargs.get('project')
        self.lists = kwargs.get('lists', [])
        self.tasks = kwargs.get('tasks', [])

    def add_list(self, task_list):
        self.lists.append(task_list)
        self.project.lists.append(task_list.unique_id)

    def edit_list(self, task_list_id, new_name):
        task_list = self._get_task_list_by_id(task_list_id)
        if task_list is not None and new_name is not None:
            task_list.name = new_name

    def remove_list(self, task_list_id):
        self.free_tasks_list(task_list_id)
        self.project.lists.remove(task_list_id)
        self.lists = [task_list for task_list in self.lists if task_list.unique_id != task_list_id]

    def add_task(self, task_list_id, task):
        task_list = self._get_task_list_by_id(task_list_id)
        if task_list is not None:
            self.tasks.append(task)
            task_list.tasks_list.append(task.unique_id)

    def remove_task(self, task_id):
        for task_list in self.lists:
            task_list.tasks_list.remove(task_id)
        self.tasks = [task for task in self.tasks if task.unique_id != task_id]

    def edit_task(self, **kwargs):
        task_id = kwargs.get('task_id')
        task = self._get_task_by_id(task_id)
        if task is None:
            return

        name = kwargs.get('name')
        if name is not None:
            task.name = name

        description = kwargs.get('description')
        if description is not None:
            task.description = description

        status = kwargs.get('status')
        if status is not None:
            task.status = status

        priority = kwargs.get('priority')
        if priority is not None:
            task.priority = priority

        expiration_date = kwargs.get('expiration_date')
        if expiration_date is not None:
            task.expiration_date = expiration_date

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

    # def add_upr(self, upr):
    #     self.project.user_project_relations_list.append(upr)

    def _get_task_list_by_id(self, task_list_id):
        if task_list_id is None:
            return None
        return next((x for x in self.lists if x.unique_id == task_list_id), None)

    def _get_task_by_id(self, task_id):
        if task_id is None:
            return None
        return next((x for x in self.tasks if x.unique_id == task_id), None)
