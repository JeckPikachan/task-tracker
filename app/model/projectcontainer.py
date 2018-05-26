import time


class ProjectContainer:
    """

    Project container unites the whole project in
    one object. It includes methods to manage the
    whole project.
    """

    # region magic methods

    def __init__(self, **kwargs):
        self.project = kwargs.get('project')
        self.lists = kwargs.get('lists', [])
        self.tasks = kwargs.get('tasks', [])
        self.plans = kwargs.get('plans', [])

    # endregion
    # region add/remove methods
    # region list

    def add_list(self, task_list):
        self.lists.append(task_list)
        self.project.lists.append(task_list.unique_id)

    def remove_list(self, task_list_id):
        self.free_tasks_list(task_list_id)
        self.project.lists.remove(task_list_id)
        self.lists = [task_list for task_list in self.lists if
                      task_list.unique_id != task_list_id]

    # endregion
    # region task
    def add_task(self, task_list_id, task):
        task_list = self._get_task_list_by_id(task_list_id)
        if task_list is not None:
            self.tasks.append(task)
            task_list.tasks_list.append(task.unique_id)
        else:
            raise ValueError("No task list with such id")

    def remove_task(self, task_id):
        for task_list in self.lists:
            task_list.tasks_list.remove(task_id)
        self.tasks = [task for task in self.tasks if task.unique_id != task_id]

    # endregion
    # region relation

    def add_relation(self, from_id, to_id, description=None):
        from_task = self.get_task_by_id(from_id)
        to_task = self.get_task_by_id(to_id)
        if from_task is None or to_task is None:
            raise NameError("No task(s) with such id")
        if to_task.unique_id in [x.to for x in from_task.related_tasks_list]:
            raise NameError("Such relation already exists")
        return from_task.add_relation(to_id, description)

    def remove_relation(self, from_id, to_id):
        from_task = self.get_task_by_id(from_id)
        if from_task is None:
            raise NameError("No task with such id")
        from_task.remove_relation(to_id)

    # endregion
    # region plan

    def add_plan(self, task_list_id, plan):
        task_list = self._get_task_list_by_id(task_list_id)
        if task_list is not None:
            self.plans.append(plan)
        else:
            raise ValueError("No task list with such id")

    def remove_plan(self, plan_id):
        self.plans = [plan for plan in
                      self.plans if plan.unique_id != plan_id]

    # endregion
    # endregion
    # region edit methods

    def edit_list(self, task_list_id, new_name):
        task_list = self._get_task_list_by_id(task_list_id)
        if task_list is not None and new_name is not None:
            task_list.name = new_name

    def edit_task(self, **kwargs):
        task_id = kwargs.get('task_id')
        task = self.get_task_by_id(task_id)
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
        self.tasks = [task for task in self.tasks if
                      task.unique_id not in task_list.tasks_list]
        task_list.tasks_list.clear()

    # endregion
    # region get methods
    def get_tasks(self, task_list_id=None):
        self._check_plans()
        if task_list_id is None:
            return self.tasks
        else:
            task_list = self._get_task_list_by_id(task_list_id)
            if task_list is not None:
                return [task for task in self.tasks if
                        task.unique_id in task_list.tasks_list]
            return None

    def _get_task_list_by_id(self, task_list_id):
        if task_list_id is None:
            return None
        return next((x for x in self.lists if x.unique_id == task_list_id), None)

    def get_task_by_id(self, task_id):
        if task_id is None:
            return None
        return next((x for x in self.tasks if x.unique_id == task_id), None)

    def get_plans(self):
        return self.plans

    def get_plan_by_id(self, plan_id):
        if plan_id is None:
            return None
        return next((x for x in self.plans if x.unique_id == plan_id), None)

    # endregion

    def _check_plans(self):
        for plan in self.plans:
            tasks, task_list_id = plan.get_planned_tasks(time.time())
            task_list = self._get_task_list_by_id(task_list_id)
            if task_list is not None:
                for task in tasks:
                    self.add_task(task_list_id, task)
            else:
                self.plans.remove(plan)
