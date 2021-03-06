import copy
import logging
import os

from adastra_library import Project, Tracker
from adastra_library import TaskList
from adastra_library.models.plan_manager import PlanManager
from adastra_library.models.project_container import ProjectContainer
from adastra_library.models.task import Task
from adastra_library.models.task_pattern import TaskPattern
from adastra_library.models.user import User
from database.tracker import TrackerDAO

from comand_line_interface.app.log_config import LOG_CONFIG
from library_util.log import log_func, init_logging


CLI_LOGGER_NAME = __name__


class NoContainerError(AttributeError):
    def __init__(self, message):
        self.message = message


def check_attribute(*attributes):
    """
    Decorator to check whether some attribute is defined
    before executing method

    :param attributes: args of str type
    :return: sets a wrapper on method
    """
    def _check_attribute(func):
        def wrapper(self, *args, **kwargs):
            flag = True
            not_chosen = ""
            for attr in attributes:
                if getattr(self, attr) is None:
                    flag = False
                    not_chosen = attr
                    break
            if flag:
                return func(self, *args, **kwargs)
            else:
                raise AttributeError("Not chosen: " + not_chosen)

        wrapper.__name__ = func.__name__
        return wrapper

    return _check_attribute


class App:
    """

    App class represent Task Tracker Library interface to use
    wherever in other projects. It doesn't implements any
    user interface.
    """
    # region magic methods
    def __init__(self, log_config=None):
        log_config = log_config if log_config is not None else LOG_CONFIG
        log_path = (log_config['log_path'] if
                    log_config.get('log_path', None) is not None else
                    os.path.dirname(__file__) + '/adastra.log')

        init_logging(log_config['level'],
                     log_path,
                     log_config['format'],
                     log_config['datefmt'])

        logging.info("App started")
        tracker_dao = TrackerDAO()
        self._tracker = Tracker(tracker_dao)
        self.user = self._tracker.get_user()
        self.uprs_collection = self._tracker.get_uprs()
        self.container = ProjectContainer(self._tracker)

    def __del__(self):
        logging.info("App is about to finish")
    # endregion
    # region add/remove methods
    # region user

    @log_func(CLI_LOGGER_NAME)
    def add_user(self, name):
        new_user = User(name=name)
        self._tracker.save_user(new_user)

    # endregion
    # region relation

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def add_relation(self, from_id, to_id, description=None):
        self.container.add_relation(from_id, to_id, description)

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def remove_relation(self, from_id, to_id):
        self.container.remove_relation(from_id, to_id)

    # endregion
    # region project

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user")
    def add_project(self, name):
        new_project = Project(name=name)
        self._tracker.add_project(new_project)
        current_user_id = self.user.unique_id
        self.uprs_collection.add_upr(current_user_id, new_project.unique_id)
        self._tracker.save_uprs(self.uprs_collection)

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user")
    def remove_project(self, project_id):
        if not self._has_user_access(project_id):
            raise PermissionError("Access denied to project with id: " + project_id)
        else:
            self.uprs_collection.remove_by_project_id(project_id)
            if self.container.get_current_project_id() == project_id:
                self.container = None
            self._tracker.remove_project(project_id)

    # endregion
    # region upr

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user")
    def add_upr(self, user_id, project_id):
        if not self._has_user_access(project_id):
            raise PermissionError("Access denied to project with id: " + project_id)
        upr = self._find_upr(user_id, project_id)
        if upr is None:
            self.uprs_collection.add_upr(user_id, project_id)
            self._tracker.save_uprs(self.uprs_collection)

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user")
    def remove_upr(self, user_id, project_id):
        if not self._has_user_access(project_id):
            raise PermissionError("Access denied to project with id: " + project_id)
        self.uprs_collection.remove_upr(user_id, project_id)
        self._tracker.save_uprs(self.uprs_collection)
        if user_id == self.user.unique_id and\
                self.container and\
                project_id == self.container.get_current_project_id():
            self._tracker.tracker_data.current_project_id = None
            self.container = None
            self._tracker.save_tracker_data()

    # endregion
    # region list

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def add_list(self, name):
        new_list = TaskList(name=name)
        self.container.add_list(new_list)

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def remove_list(self, task_list_id):
        self.container.remove_list(task_list_id)

    # endregion
    # region task

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def add_task(self, task_list_id, name, **kwargs):
        new_task = Task(name=name, author=self.user.unique_id, **kwargs)
        self.container.add_task(task_list_id, new_task)

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def remove_task(self, task_id):
        self.container.remove_task(task_id)

    # endregion
    # region plan

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user", "container")
    def add_plan(self,
                 name,
                 task_list_id,
                 delta,
                 status=None,
                 priority=None,
                 description=None,
                 start_date=None,
                 end_date=None):
        task_pattern = TaskPattern(name, description, priority, status, self.user.unique_id)
        new_plan = PlanManager(delta, task_pattern, task_list_id, start_date, end_date)
        self.container.add_plan(task_list_id, new_plan)

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user", "container")
    def remove_plan(self, plan_id):
        self.container.remove_plan(plan_id)

    # endregion
    # endregion
    # region change/checkout methods

    @log_func(CLI_LOGGER_NAME)
    def change_user(self, user_id):
        self.user = self._tracker.get_user(user_id)
        self.container.leave_project()
        self.container = None

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user")
    def load_project(self, project_id):
        has_access = self._has_user_access(project_id)
        if has_access:
            self.container = ProjectContainer(self._tracker)
            self.container.load(project_id)
        else:
            raise PermissionError("Access denied to project with id: " + project_id)

    # endregion
    # region get methods
    # region project

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def get_current_project(self):
        return copy.deepcopy(self.container.get_current_project())

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user")
    def get_projects_info(self):
        projects_info, current_project_id = self._tracker.get_projects_info()
        return ([x for x in projects_info if
                 self._has_user_access(x['unique_id'])],
                current_project_id)

    # endregion
    # region user

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user")
    def get_user(self):
        return copy.deepcopy(self.user)

    @log_func(CLI_LOGGER_NAME)
    def get_users_info(self):
        return self._tracker.get_users_info()

    # endregion
    # region list

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def get_task_lists(self):
        return copy.deepcopy(self.container.get_task_lists())

    # endregion
    # region plan

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user", "container")
    def get_plans(self):
        return copy.deepcopy(self.container.get_plans())

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("user", "container")
    def get_plan_by_id(self, plan_id):
        return copy.deepcopy(self.container.get_plan_by_id(plan_id))

    # endregion
    # region task

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def get_tasks(self, task_list_id=None):
        tasks = copy.deepcopy(self.container.get_tasks(task_list_id))
        return tasks

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def get_task_by_id(self, task_id):
        return self.container.get_task_by_id(task_id)

    # endregion
    # endregion
    # region edit methods

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def edit_project(self, new_name):
        if new_name is not None:
            self.container.edit_project(new_name)

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def edit_task_list(self, task_list_id, new_name):
        self.container.edit_list(task_list_id, new_name)

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def edit_task(self, **kwargs):
        self.container.edit_task(**kwargs)

    @log_func(CLI_LOGGER_NAME)
    @check_attribute("container", "user")
    def free_tasks_list(self, task_list_id):
        self.container.free_tasks_list(task_list_id)

    # endregion
    # region private methods

    def _has_user_access(self, project_id):
        upr = self._find_upr(self.user.unique_id, project_id)
        return upr is not None

    def _find_upr(self, user_id, project_id):
        return next((x for x in self.uprs_collection.uprs if
                    x.project_id == project_id and x.user_id == user_id), None)

    # endregion
