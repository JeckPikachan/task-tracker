import json

from model.project import Project


class DBConfig:
    def __init__(self, current_project_id=None):
        self.current_project_id = current_project_id


class DataBase:
    def __init__(self):
        self.project = None
        try:
            with open("./db_config.json","r") as config_file:
                self.config = DBConfig(**json.load(config_file))
        except IOError:
            self.config = DBConfig()

    def load_from_file(self, project_id):
        try:
            with open("../database/projects/" + project_id + ".json", "r") as project_file:
                self.project = Project(**json.load(project_file))
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
            return self.load_from_file(project_id)

    def save(self, project=None):
        project = project if project is not None else self.project
        try:

            with open("../database/projects/" + str(project.unique_id) + ".json", "w+") as project_file:
                json.dump(self.json_serializable(project), project_file, indent=4)
            return None
        except IOError as e:
            return e

    def add(self, project):
        return self.save(project)

    def json_serializable(self, obj):
        new_dict = obj.__dict__ or obj
        return new_dict
