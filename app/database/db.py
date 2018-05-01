import json

import copy

from app.model.projectcontainer import ProjectContainer
from app.model.project import Project
from app.model.task import Task
from app.model.tasklist import TaskList
from app.util.enum_json import enum_serializable


class DBConfig:
    def __init__(self, current_project_id=None):
        self.current_project_id = current_project_id


class DataBase:
    def __init__(self, db_path):
        self.project = None
        self._task_lists = []
        self._tasks = []
        self._db_path = db_path
        try:
            with open(self._db_path + "db_config.json","r") as config_file:
                self.config = DBConfig(**json.load(config_file))
        except IOError:
            self.config = DBConfig()

    def load_from_file(self, project_id):
        try:
            with open(self._db_path + "projects/" + project_id + ".json", "r") as project_file:
                loaded = json.load(project_file)
                project = loaded.get('project')
                lists = loaded.get('task_lists', [])
                tasks = loaded.get('tasks', [])

                loaded['project'] = Project(**project)
                loaded['lists'] = [TaskList(**task_list) for task_list in lists]
                loaded['tasks'] = [Task(**task) for task in tasks]
                container = ProjectContainer(**loaded)

                self.config.current_project_id = project.get('unique_id')
            return container
        except IOError as e:
            raise

    def load(self, project_id=None):
        if project_id is None:
            current_project_id = self.config.current_project_id

            if current_project_id is not None:
                return self.load_from_file(current_project_id)
            return None

        else:
            container = self.load_from_file(project_id)
            if container is not None:
                self.save_config()
            return container

    def save(self, container):
        container = copy.deepcopy(container)
        tasks = [self._task_serializable(task) for task in container.tasks]
        task_lists = [self._json_serializable(task_list) for task_list in container.lists]
        project = self._json_serializable(container.project)

        dict_to_save = {'project': project, 'task_lists': task_lists, 'tasks': tasks}

        try:
            with open(self._db_path + "projects/" + str(project.get('unique_id')) + ".json", "w+") as project_file:
                json.dump(dict_to_save, project_file, indent=4)
            return None
        except IOError as e:
            return e

    def save_config(self):
        try:
            with open(self._db_path + "db_config.json", "w+") as config_file:
                json.dump(self._json_serializable(self.config), config_file, indent=4)
            return None
        except IOError as e:
            return e

    def _json_serializable(self, obj):
        new_dict = obj.__dict__ or obj
        return new_dict

    def _task_serializable(self, task):
        task_dict = self._json_serializable(task)
        task_dict['status'] = enum_serializable(task_dict['status'])
        task_dict['priority'] = enum_serializable(task_dict['priority'])
        return task_dict
