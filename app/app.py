from database.db import DataBase
from model.project import Project
from model.tasklist import TaskList


class App:
    def __init__(self):
        self._db = DataBase()
        self._db.load()

    def add_project(self, name):
        new_project = Project(name=name)
        self._db.add(new_project)

    def load_project(self, project_id):
        self._db.load(project_id)

    def add_list(self, name):
        new_list = TaskList(name=name)
        self._db.add_task_list(new_list)

    def get_task_lists(self):
        return self._db.get_task_lists()

    def change_task_list_name(self, task_list_id, new_name):
        self._db.change_task_list_name(task_list_id, new_name)
