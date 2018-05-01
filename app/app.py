import copy

from database.db import DataBase
from model.project import Project
from model.projectcontainer import ProjectContainer
from model.task import Task
from model.tasklist import TaskList


class App:
    def __init__(self):
        self._db = DataBase()
        self.container = self._db.load()

    def add_project(self, name):
        new_project = Project(name=name)
        new_container = ProjectContainer(project=new_project)
        self._db.save(new_container)

    def load_project(self, project_id):
        self.container = self._db.load(project_id)

    def add_list(self, name):
        new_list = TaskList(name=name)
        self.container.add_list(new_list)
        self._db.save(self.container)

    def get_task_lists(self):
        return copy.deepcopy(self.container.lists)

    def change_task_list_name(self, task_list_id, new_name):
        self.container.change_task_list_name(task_list_id, new_name)
        self._db.save(self.container)

    def add_task(self, task_list_id, name):
        new_task = Task(name=name)
        self.container.add_task(task_list_id, new_task)
        self._db.save(self.container)

    def remove_task(self, task_id):
        self.container.remove_task(task_id)
        self._db.save(self.container)

    def get_tasks(self, task_list_id=None):
        return copy.deepcopy(self.container.get_tasks(task_list_id))
