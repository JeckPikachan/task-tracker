import copy
import json
import logging

import os

from app.database.db import DataBase
from app.model.project import Project
from app.model.projectcontainer import ProjectContainer
from app.model.task import Task
from app.model.tasklist import TaskList
from app.model.user import User
from app.util.log import log_func


class NoContainerError(AttributeError):
    def __init__(self, message):
        self.message = message


def check_attribute(*attributes):
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
    def __init__(self):
        with open(os.path.dirname(__file__) + '/log_config.json', 'r') as log_config_file:
            log_config = json.load(log_config_file)

        if not log_config['level'] == 'OFF':
            logging.basicConfig(
                filename=os.path.dirname(__file__) + '/adastra.log',
                level=logging.getLevelName(log_config['level']),
                format=log_config['format'],
                datefmt=log_config['datefmt'])
        logging.info("App started")
        self._db = DataBase()
        self.user = self._db.load_user()
        self.uprs_collection = self._db.load_uprs()
        self.container = self._db.load()

    def __del__(self):
        logging.info("App is about to finish")

    @log_func
    def add_user(self, name):
        new_user = User(name=name)
        self._db.save_user(new_user)

    @log_func
    def change_user(self, user_id):
        self.user = self._db.load_user(user_id)
        self._db.leave_project()
        self.container = self._db.load()

    @log_func
    @check_attribute("user")
    def add_project(self, name):
        new_project = Project(name=name)
        new_container = ProjectContainer(project=new_project)
        current_user_id = self.user.unique_id
        self._db.save(new_container)
        self.uprs_collection.add_upr(current_user_id, new_project.unique_id)
        self._db.save_uprs(self.uprs_collection)

    @log_func
    @check_attribute("user")
    def load_project(self, project_id):
        has_access = self._has_user_access(project_id)
        if has_access:
            self.container = self._db.load(project_id)
        else:
            raise PermissionError("Access denied to project with id: " + project_id)

    @log_func
    @check_attribute("container", "user")
    def get_project(self):
        return copy.deepcopy(self.container.project)

    @log_func
    @check_attribute("user")
    def get_user(self):
        return copy.deepcopy(self.user)

    @log_func
    @check_attribute("user")
    def remove_project(self, project_id):
        self._db.remove(project_id)
        if self.container.project.unique_id == project_id:
            self.container = None

    @log_func
    @check_attribute("container", "user")
    def edit_project(self, new_name):
        if new_name is not None:
            self.container.project.name = new_name
            self._db.save(self.container)

    @log_func
    @check_attribute("container", "user")
    def add_list(self, name):
        new_list = TaskList(name=name)
        self.container.add_list(new_list)
        self._db.save(self.container)

    @log_func
    @check_attribute("container", "user")
    def get_task_lists(self):
        return copy.deepcopy(self.container.lists)

    @log_func
    @check_attribute("container", "user")
    def edit_task_list(self, task_list_id, new_name):
        self.container.edit_list(task_list_id, new_name)
        self._db.save(self.container)

    @log_func
    @check_attribute("container", "user")
    def remove_list(self, task_list_id):
        self.container.remove_list(task_list_id)
        self._db.save(self.container)

    @log_func
    @check_attribute("container", "user")
    def add_task(self, task_list_id, name, **kwargs):
        new_task = Task(name=name, **kwargs)
        self.container.add_task(task_list_id, new_task)
        self._db.save(self.container)

    @log_func
    @check_attribute("container", "user")
    def remove_task(self, task_id):
        self.container.remove_task(task_id)
        self._db.save(self.container)

    @log_func
    @check_attribute("container", "user")
    def edit_task(self, **kwargs):
        self.container.edit_task(**kwargs)
        self._db.save(self.container)

    @log_func
    @check_attribute("container", "user")
    def free_tasks_list(self, task_list_id):
        self.container.free_tasks_list(task_list_id)
        self._db.save(self.container)

    @log_func
    @check_attribute("container", "user")
    def get_tasks(self, task_list_id=None):
        return copy.deepcopy(self.container.get_tasks(task_list_id))

    def _has_user_access(self, project_id):
        upr = next((x for x in self.uprs_collection.uprs if
                    x.project_id == project_id and x.user_id == self.user.unique_id), None)
        return upr is not None

    @log_func
    @check_attribute("user")
    def get_projects_info(self):
        return ([x for x in self._db.get_config().projects_info if self._has_user_access(x['unique_id'])],
                self._db.get_config().current_project_id)

    @log_func
    def get_users_info(self):
        return [x for x in self._db.get_config().users_info], self._db.get_config().current_user_id
