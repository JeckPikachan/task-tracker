from datetime import datetime

from library_util.log import LIBRARY_LOGGER_NAME, log_func


class ProjectContainer:
    """

    Project container unites the whole project in
    one object. It includes methods to manage the
    whole project.
    """

    # region magic methods

    def __init__(self, db):
        self._db = db
        self.load()

    @log_func(LIBRARY_LOGGER_NAME)
    def load(self, project_id=None):
        self._db.load(project_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def leave_project(self):
        self._db.leave_project()
        self._db.load()

    # endregion
    # region add/remove methods
    # region list

    @log_func(LIBRARY_LOGGER_NAME)
    def add_list(self, task_list):
        """
        Adds passed task list lists list

        :param task_list: {TaskList} TaskList object to be added
        :return:
        """
        self._db.add_list(task_list)

    @log_func(LIBRARY_LOGGER_NAME)
    def remove_list(self, task_list_id):
        """
        Removes task list with specified task list id from lists list\

        :param task_list_id: {string} task list id
        :return:
        """
        self._db.remove_list(task_list_id)

    # endregion
    # region task
    @log_func(LIBRARY_LOGGER_NAME)
    def add_task(self, task_list_id, task):
        """
        Adds passed task to list with specified task list id if exists

        :param task_list_id: {string} task list id
        :param task: {Task} Task object to be added
        :return:
        """
        self._db.add_task(task_list_id, task)

    @log_func(LIBRARY_LOGGER_NAME)
    def remove_task(self, task_id):
        """
        Removes task with specified task id

        :param task_id: {string} task id
        :return:
        """
        self._db.remove_task(task_id)

    # endregion
    # region relation

    @log_func(LIBRARY_LOGGER_NAME)
    def add_relation(self, from_id, to_id, description=None):
        """
        Adds relation between two tasks

        :param from_id: {string} id of task from which relation will be set
        :param to_id: {string} id of task to which relation will be set
        :param description: {string} Describes type of relation
        :return: Created TaskRelation object
        """
        return self._db.add_relation(from_id, to_id, description)

    @log_func(LIBRARY_LOGGER_NAME)
    def remove_relation(self, from_id, to_id):
        """
        Removes relation between two tasks with specified ids

        :param from_id: {string} id of task from which relation will be unset
        :param to_id: {string} id of task to which relation will be unset
        :return:
        """
        self._db.remove_relation(from_id, to_id)

    # endregion
    # region plan

    @log_func(LIBRARY_LOGGER_NAME)
    def add_plan(self, task_list_id, plan):
        """

        :param task_list_id: {string} id of task list to which tasks
            will be added
        :param plan: {PlanManager} Plan to be added
        :return:
        """
        self._db.add_plan(task_list_id, plan)

    @log_func(LIBRARY_LOGGER_NAME)
    def remove_plan(self, plan_id):
        """
        Removes plan with specified id

        :param plan_id: {string} plan id
        :return:
        """
        self._db.remove_plan(plan_id)

    # endregion
    # endregion
    # region edit methods

    @log_func(LIBRARY_LOGGER_NAME)
    def edit_list(self, task_list_id, new_name):
        """

        :param task_list_id: {string} id of task list to be edited
        :param new_name: {string} new name
        :return:
        """
        self._db.edit_list(task_list_id, new_name)

    @log_func(LIBRARY_LOGGER_NAME)
    def edit_task(self, **kwargs):
        """

        :param kwargs: can include:
            task_id: {string} id of task to be edited
            name: {string} new name
            description: {string} new description
            status: {Status} new task status
            priority: {Priority} new task priority
            expiration_date: {date} new expiration date
        :return:
        """
        self._db.edit_task(**kwargs)

    @log_func(LIBRARY_LOGGER_NAME)
    def edit_project(self, new_name):
        self._db.edit_project(new_name)

    @log_func(LIBRARY_LOGGER_NAME)
    def free_tasks_list(self, task_list_id):
        """
        Removes all tasks from task list with specified id

        :param task_list_id: {string} task list id
        :return:
        """
        self._db.free_tasks_list(task_list_id)

    # endregion
    # region get methods
    @log_func(LIBRARY_LOGGER_NAME)
    def get_tasks(self, task_list_id=None):
        """

        :param task_list_id: {string} task list id
        :return: All project tasks or from specified task list only
        """
        self._check_plans()
        return self._db.get_tasks(task_list_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def get_task_by_id(self, task_id):
        """

        :param task_id: {string} id of task
        :return: task with passed id or None
        """
        return self._db.get_task_by_id(task_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def get_task_lists(self):
        return self._db.get_task_lists()

    @log_func(LIBRARY_LOGGER_NAME)
    def get_plans(self):
        """

        :return: All plans
        """
        return self._db.get_plans()

    @log_func(LIBRARY_LOGGER_NAME)
    def get_plan_by_id(self, plan_id):
        """

        :param plan_id: {string} plan id
        :return: Plan with passed id or None
        """
        self._db.get_plan_by_id(plan_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def get_current_project_id(self):
        """

        :return: id of current project
        """
        return self._db.get_projects_info()[1]

    @log_func(LIBRARY_LOGGER_NAME)
    def get_current_project(self):
        """

        :return: instance of current project
        """
        return self._db.get_current_project()

    # endregion

    def _check_plans(self):
        plans = self._db.get_plans()
        for plan in plans:
            tasks, task_list_id = plan.get_planned_tasks(datetime.now())
            task_list = self._db.get_task_list_by_id(task_list_id)
            if task_list is not None:
                for task in tasks:
                    self.add_task(task_list_id, task)
            else:
                self._db.remove_plan(plan.unique_id)
