import json

from model.project import Project
from model.tasklist import TaskList


class DBConfig:
    def __init__(self, current_project_id=None):
        self.current_project_id = current_project_id


class DataBase:
    def __init__(self):
        self.project = None
        self._task_lists = []
        self._tasks = []
        try:
            with open("../database/db_config.json","r") as config_file:
                self.config = DBConfig(**json.load(config_file))
        except IOError:
            self.config = DBConfig()

    def load_from_file(self, project_id):
        try:
            with open("../database/projects/" + project_id + ".json", "r") as project_file:
                loaded = json.load(project_file)
                project = loaded.get('project')
                lists = loaded.get('task_lists', [])

                self.project = Project(**project)
                self._task_lists = [TaskList(**task_list) for task_list in lists]

                self.config.current_project_id = self.project.unique_id
            return None
        except IOError as e:
            return e

    def load(self, project_id=None):
        if project_id is None:
            current_project_id = self.config.current_project_id

            if current_project_id is not None:
                return self.load_from_file(current_project_id)
            return None

        else:
            error = self.load_from_file(project_id)
            if error is None:
                self.save_config()
            return error

    def save(self, project=None):
        task_lists = [] if project is not None \
            else [self.json_serializable(task_list) for task_list in self._task_lists]
        project = self.json_serializable(project if project is not None else self.project)

        dict_to_save = {'project': project, 'task_lists': task_lists}

        try:
            with open("../database/projects/" + str(project.get('unique_id')) + ".json", "w+") as project_file:
                json.dump(dict_to_save, project_file, indent=4)
            return None
        except IOError as e:
            return e

    def save_config(self):
        try:
            with open("../database/db_config.json", "w+") as config_file:
                json.dump(self.json_serializable(self.config), config_file, indent=4)
            return None
        except IOError as e:
            return e

    def add(self, project):
        return self.save(project)

    def add_task_list(self, task_list):
        self._task_lists.append(task_list)
        self.project.lists.append(task_list.unique_id)
        self.save()

    def get_task_lists(self):
        return [{'unique_id': task_list.unique_id, 'name': task_list.name} for task_list in self._task_lists]

    def change_task_list_name(self, task_list_id, new_name):
        task_list = next((x for x in self._task_lists if x.unique_id == task_list_id), None)
        if task_list is not None:
            task_list.name = new_name
            self.save()

    def json_serializable(self, obj):
        new_dict = obj.__dict__ or obj
        return new_dict
