import copy

from app.database.db import DataBase
from app.model.project import Project
from app.model.projectcontainer import ProjectContainer
from app.model.task import Task
from app.model.tasklist import TaskList


class NoContainerError(AttributeError):
    def __init__(self, message):
        self.message = message


def check_attribute(attribute):
    def _check_attribute(func):
        def wrapper(self, *args, **kwargs):
            if getattr(self, attribute) is not None:
                return func(self, *args, **kwargs)
            else:
                raise NoContainerError("ERROR: Please choose project before making any actions.")

        return wrapper

    return _check_attribute


class App:
    def __init__(self, app_path):
        self._db = DataBase(app_path + "database/")
        self.container = self._db.load()

    def add_project(self, name):
        new_project = Project(name=name)
        new_container = ProjectContainer(project=new_project)
        self._db.save(new_container)

    def load_project(self, project_id):
        self.container = self._db.load(project_id)

    @check_attribute("container")
    def get_project(self):
        return copy.deepcopy(self.container.project)

    def remove_project(self, project_id):
        self._db.remove(project_id)
        if self.container.project.unique_id == project_id:
            self.container = None

    @check_attribute("container")
    def edit_project(self, new_name):
        if new_name is not None:
            self.container.project.name = new_name
            self._db.save(self.container)

    @check_attribute("container")
    def add_list(self, name):
        new_list = TaskList(name=name)
        self.container.add_list(new_list)
        self._db.save(self.container)

    @check_attribute("container")
    def get_task_lists(self):
        return copy.deepcopy(self.container.lists)

    @check_attribute("container")
    def edit_task_list(self, task_list_id, new_name):
        self.container.edit_task_list(task_list_id, new_name)
        self._db.save(self.container)

    @check_attribute("container")
    def remove_list(self, task_list_id):
        self.container.remove_list(task_list_id)
        self._db.save(self.container)

    @check_attribute("container")
    def add_task(self, task_list_id, name, **kwargs):
        new_task = Task(name=name, **kwargs)
        self.container.add_task(task_list_id, new_task)
        self._db.save(self.container)

    @check_attribute("container")
    def remove_task(self, task_id):
        self.container.remove_task(task_id)
        self._db.save(self.container)

    @check_attribute("container")
    def free_tasks_list(self, task_list_id):
        self.container.free_tasks_list(task_list_id)
        self._db.save(self.container)

    @check_attribute("container")
    def get_tasks(self, task_list_id=None):
        return copy.deepcopy(self.container.get_tasks(task_list_id))

    def get_projects_info(self):
        return self._db.get_config()
