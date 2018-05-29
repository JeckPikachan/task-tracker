import copy
import json
import os

from adastra_library import Project, TaskList, Task, TaskPattern, PlanManager, ProjectContainer, User, UPRSCollection
from util.log import log_func
from util.enum_json import enum_serializable, as_enum


class DBConfig:
    # region magic methods

    def __init__(self, current_project_id=None, current_user_id=None,
                 projects_info=None, users_info=None):
        self.current_project_id = current_project_id
        self.current_user_id = current_user_id
        self.projects_info = projects_info if projects_info is not None else []
        self.users_info = users_info if users_info is not None else []

    # endregion
    # region add methods

    def add_project_info(self, name, unique_id):
        found = next((x for x in self.projects_info if
                      x['unique_id'] == unique_id),
                     None)
        if found is None:
            self.projects_info.append({'unique_id': unique_id, 'name': name})
        else:
            found['name'] = name

    def add_user_info(self, name, unique_id):
        found = next((x for x in self.users_info if x['unique_id'] == unique_id),
                     None)
        if found is None:
            self.users_info.append({'unique_id': unique_id, 'name': name})
        else:
            found['name'] = name

    # endregion


class DataBase:
    """

    DataBase class is used to manage simple json data base
    and to encapsulate operations on json files.
    """

    # region magic methods

    def __init__(self, config=None):
        self._db_path = (config.db_path if config is not None and
                         config.db_path is not None else
                         os.path.dirname(__file__) + "/data/")
        try:
            with open(self._db_path + "db_info.json", "r") as config_file:
                self.config = DBConfig(**json.load(config_file))
        except IOError:
            self.config = DBConfig()

    # endregion
    # region load methods
    def load_from_file(self, project_id):
        try:
            with open(self._db_path + "projects/" + project_id + ".json", "r") as \
                    project_file:
                loaded = json.load(project_file)
                project = loaded.get('project')
                lists = loaded.get('task_lists', [])
                tasks = loaded.get('tasks', [])
                for task in tasks:
                    task['status'] = as_enum(task['status'])
                    task['priority'] = as_enum(task['priority'])
                loaded_plans = loaded.get('plans', [])

                loaded['project'] = Project(**project)
                loaded['lists'] = [TaskList(**task_list) for task_list in lists]
                loaded['tasks'] = [Task(**task) for task in tasks]

                plans = []
                for plan in loaded_plans:
                    task_pattern = TaskPattern(**plan.get('task_pattern'))
                    plan['task_pattern'] = task_pattern
                    plans.append(PlanManager(**plan))

                loaded['plans'] = plans

                container = ProjectContainer(**loaded)

                self.config.current_project_id = project.get('unique_id')
            return container
        except IOError as e:
            raise

    @log_func
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

    @log_func
    def load_user(self, user_id=None):
        if user_id is None:
            user_id = self.config.current_user_id
            if user_id is None:
                return None
        try:
            with open(self._db_path + "users/" + user_id + ".json", "r") as user_file:
                loaded = json.load(user_file)
                user = User(**loaded)
                self.config.current_user_id = user_id
                self.save_config()
            return user
        except IOError as e:
            raise e

    @log_func
    def load_uprs(self):
        try:
            with open(self._db_path + "uprs/uprs.json", "r") as uprs_file:
                loaded = json.load(uprs_file)
                uprs_collection = UPRSCollection(**loaded)
            return uprs_collection
        except IOError as e:
            raise e

    # endregion
    # region save methods

    @log_func
    def save(self, container):
        container = copy.deepcopy(container)
        tasks = [Serialization.task_serializable(task) for task in container.tasks]
        task_lists = [Serialization.json_serializable(task_list) for
                      task_list in container.lists]
        project = Serialization.project_serializable(container.project)
        plans = [Serialization.plan_serializable(plan) for plan in container.plans]

        project_name = project.get('name')
        project_id = project.get('unique_id')

        dict_to_save = \
            {'project': project, 'task_lists': task_lists, 'tasks': tasks, 'plans': plans}

        try:
            with open(self._db_path + "projects/" + project_id + ".json", "w+") as \
                    project_file:
                json.dump(dict_to_save, project_file, indent=4)

            self.config.add_project_info(project_name, project_id)
            self.save_config()
            return None
        except IOError as e:
            return e

    @log_func
    def save_config(self):
        try:
            with open(self._db_path + "db_info.json", "w+") as config_file:
                json.dump(Serialization.json_serializable(self.config),
                          config_file, indent=4)
            return None
        except IOError as e:
            return e

    @log_func
    def save_user(self, user):
        try:
            with open(self._db_path + "users/" + user.unique_id + ".json", "w+") as \
                    user_file:
                json.dump(Serialization.json_serializable(user), user_file, indent=4)
            self.config.add_user_info(user.name, user.unique_id)
            self.save_config()
            return None
        except IOError as e:
            return e

    @log_func
    def save_uprs(self, uprs_collection):
        try:
            with open(self._db_path + "uprs/uprs.json", "w+") as uprs_file:
                json.dump(Serialization.uprs_collection_serializable(uprs_collection),
                          uprs_file, indent=4)
            return None
        except IOError as e:
            return e

    # endregion
    # region remove methods

    @log_func
    def remove(self, project_id):
        try:
            os.remove(self._db_path + "projects/" + project_id + ".json")
            self.config.projects_info = \
                [project_info for project_info in
                 self.config.projects_info if
                 project_info.get('unique_id') != project_id]
            if self.config.current_project_id == project_id:
                self.config.current_project_id = None
            self.save_config()
        except OSError:
            pass

    # endregion
    # region get methods

    @log_func
    def get_config(self):
        return copy.copy(self.config)

    # endregion
    # region change methods

    @log_func
    def leave_project(self):
        self.config.current_project_id = None
        self.save_config()

    # endregion


class Serialization:
    @staticmethod
    def json_serializable(obj):
        new_dict = obj.__dict__ or obj
        return new_dict

    @staticmethod
    def project_serializable(project):
        return project.__dict__

    @staticmethod
    def uprs_collection_serializable(uprs_collection):
        uprs_collection.uprs = [Serialization.json_serializable(upr) for upr in
                                uprs_collection.uprs]
        return uprs_collection.__dict__

    @staticmethod
    def plan_serializable(plan):
        plan.task_pattern = Serialization.json_serializable(plan.task_pattern)
        return Serialization.json_serializable(plan)

    @staticmethod
    def task_serializable(task):
        task_dict = Serialization.json_serializable(task)
        task_dict['status'] = enum_serializable(task_dict['_status'])
        task_dict['priority'] = enum_serializable(task_dict['_priority'])
        task_dict['expiration_date'] = '{0:%Y-%m-%d %H:%M}' \
            .format(task_dict['_expiration_date']) if \
            task_dict['_expiration_date'] is not None else None
        del task_dict['_expiration_date']
        del task_dict['_status']
        del task_dict['_priority']
        task_dict['related_tasks_list'] = [Serialization.json_serializable(x) for
                                           x in task_dict['related_tasks_list']]

        return task_dict
