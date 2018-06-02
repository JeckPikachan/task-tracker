import copy
import json
import os
from datetime import datetime

from adastra_library import Project, TaskList, Task, TaskPattern, PlanManager, ProjectContainer, User, UPRCollection
from database import serialization
from util.enum_json import as_enum
from util.find import find_one_in_dicts, find_one
from util.log import log_func


class DBInfo:
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
        found = find_one_in_dicts(self.projects_info, unique_id)
        if found is None:
            self.projects_info.append({'unique_id': unique_id, 'name': name})
        else:
            found['name'] = name

    def add_user_info(self, name, unique_id):
        found = find_one_in_dicts(self.users_info, unique_id)
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
        self._db_path = (config.get('db_path') if config is not None and
                         config.get('db_path', None) is not None else
                         os.path.dirname(__file__) + "/data/")
        try:
            with open(self._db_path + "db_info.json", "r") as config_file:
                self.db_info = DBInfo(**json.load(config_file))
        except IOError:
            self.db_info = DBInfo()

        self._project = Project()
        self._task_lists = []
        self._tasks = []
        self._plans = []

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

                self._project = Project(**project)
                self._task_lists = [TaskList(**task_list) for task_list in lists]
                self._tasks = [Task(**task) for task in tasks]

                plans = []
                for plan in loaded_plans:
                    task_pattern = TaskPattern(**plan.get('task_pattern'))
                    plan['task_pattern'] = task_pattern
                    plan['start_date'] = datetime.fromtimestamp(plan['start_date']) if \
                        plan['start_date'] is not None else None
                    plan['end_date'] = datetime.fromtimestamp(plan['end_date']) if \
                        plan['end_date'] is not None else None
                    plan['last_created'] = datetime.fromtimestamp(plan['last_created']) if \
                        plan['last_created'] is not None else None
                    plans.append(PlanManager(**plan))

                self._plans = plans

                self.db_info.current_project_id = project.get('unique_id')
            return self.db_info.current_project_id
        except IOError as e:
            raise e

    @log_func
    def load(self, project_id=None):
        if project_id is None:
            current_project_id = self.db_info.current_project_id

            if current_project_id is not None:
                self.load_from_file(current_project_id)

        else:
            new_current_project_id = self.load_from_file(project_id)
            if new_current_project_id is not None:
                self.save_db_info()

    @log_func
    def load_user(self, user_id=None):
        if user_id is None:
            user_id = self.db_info.current_user_id
            if user_id is None:
                return None
        try:
            with open(self._db_path + "users/" + user_id + ".json", "r") as user_file:
                loaded = json.load(user_file)
                user = User(**loaded)
                self.db_info.current_user_id = user_id
                self.save_db_info()
            return user
        except IOError as e:
            raise e

    @log_func
    def load_uprs(self):
        try:
            with open(self._db_path + "uprs/uprs.json", "r") as uprs_file:
                loaded = json.load(uprs_file)
                uprs_collection = UPRCollection(**loaded)
            return uprs_collection
        except IOError as e:
            raise e

    # endregion
    # region save methods

    @log_func
    def save(self):
        tasks = [serialization.transform_task(task) for task in self._tasks]
        task_lists = [serialization.transform_object(task_list) for
                      task_list in self._task_lists]
        project = serialization.transform_project(self._project)
        plans = [serialization.transform_plan(plan) for plan in self._plans]

        project_name = project.get('name')
        project_id = project.get('unique_id')

        dict_to_save = \
            {'project': project, 'task_lists': task_lists, 'tasks': tasks, 'plans': plans}

        try:
            with open(self._db_path + "projects/" + project_id + ".json", "w+") as \
                    project_file:
                json.dump(dict_to_save, project_file, indent=4)

            self.db_info.add_project_info(project_name, project_id)
            self.save_db_info()
            return None
        except IOError as e:
            return e

    @log_func
    def save_db_info(self):
        try:
            with open(self._db_path + "db_info.json", "w+") as config_file:
                json.dump(serialization.transform_object(self.db_info),
                          config_file, indent=4)
            return None
        except IOError as e:
            return e

    @log_func
    def save_user(self, user):
        try:
            with open(self._db_path + "users/" + user.unique_id + ".json", "w+") as \
                    user_file:
                json.dump(serialization.transform_object(user), user_file, indent=4)
            self.db_info.add_user_info(user.name, user.unique_id)
            self.save_db_info()
            return None
        except IOError as e:
            return e

    @log_func
    def save_uprs(self, uprs_collection):
        try:
            with open(self._db_path + "uprs/uprs.json", "w+") as uprs_file:
                json.dump(serialization.transform_upr_collection(uprs_collection),
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
            self.db_info.projects_info = \
                [project_info for project_info in
                 self.db_info.projects_info if
                 project_info.get('unique_id') != project_id]
            if self.db_info.current_project_id == project_id:
                self.db_info.current_project_id = None
            self.save_db_info()
        except OSError:
            pass

    # endregion
    # region get methods

    @log_func
    def get_projects_info(self):
        return (self.db_info.projects_info,
                self.db_info.current_project_id)

    def get_current_project(self):
        return self._project

    @log_func
    def get_users_info(self):
        return (self.db_info.users_info,
                self.db_info.current_user_id)

    # endregion
    # region change methods

    @log_func
    def leave_project(self):
        self.db_info.current_project_id = None
        self.save_db_info()

    # endregion
    # region API

    @log_func
    def add_project(self, project):
        dict_to_save = {'project': serialization.transform_project(project)}
        project_id = project.unique_id
        project_name = project.name

        try:
            with open(self._db_path + "projects/" + project_id + ".json", "w+") as \
                    project_file:
                json.dump(dict_to_save, project_file, indent=4)

            self.db_info.add_project_info(project_name, project_id)
            self.save_db_info()
            return None
        except IOError as e:
            return e

    @log_func
    def add_list(self, task_list):
        self._task_lists.append(task_list)
        self._project.lists.append(task_list.unique_id)
        self.save()

    @log_func
    def remove_list(self, task_list_id):
        self.free_tasks_list(task_list_id)
        self._project.lists.remove(task_list_id)
        self._task_lists = [task_list for task_list in self._task_lists if
                            task_list.unique_id != task_list_id]
        self.save()

    @log_func
    def add_task(self, task_list_id, task):
        task_list = self.get_task_list_by_id(task_list_id)
        if task_list is not None:
            self._tasks.append(task)
            task_list.tasks_list.append(task.unique_id)
        else:
            raise ValueError("No task list with such id")
        self.save()

    @log_func
    def remove_task(self, task_id):
        for task_list in self._task_lists:
            if task_id in task_list.tasks_list:
                task_list.tasks_list.remove(task_id)
        self._tasks = [task for task in self._tasks if
                       task.unique_id != task_id]
        self.save()

    @log_func
    def add_relation(self, from_id, to_id, description=None):
        from_task = self.get_task_by_id(from_id)
        to_task = self.get_task_by_id(to_id)
        if from_task is None or to_task is None:
            raise NameError("No task(s) with such id")
        if to_task.unique_id in [x.to for x in from_task.related_tasks_list]:
            raise NameError("Such relation already exists")
        new_relation = from_task.add_relation(to_id, description)
        self.save()
        return new_relation

    @log_func
    def remove_relation(self, from_id, to_id):
        from_task = self.get_task_by_id(from_id)
        if from_task is None:
            raise NameError("No task with such id")
        from_task.remove_relation(to_id)
        self.save()

    @log_func
    def add_plan(self, task_list_id, plan):
        task_list = self.get_task_list_by_id(task_list_id)
        if task_list is not None:
            self._plans.append(plan)
        else:
            raise ValueError("No task list with such id")
        self.save()

    @log_func
    def remove_plan(self, plan_id):
        self._plans = [plan for plan in
                       self._plans if plan.unique_id != plan_id]
        self.save()

    @log_func
    def edit_list(self, task_list_id, new_name):
        task_list = self.get_task_list_by_id(task_list_id)
        if task_list is not None and new_name is not None:
            task_list.name = new_name
        self.save()

    @log_func
    def edit_task(self, task_id, **kwargs):
        task = self.get_task_by_id(task_id)
        if task is None:
            return

        name = kwargs.get('name')
        if name is not None:
            task.name = name

        description = kwargs.get('description')
        if description is not None:
            task.description = description

        status = kwargs.get('status')
        if status is not None:
            task.status = status

        priority = kwargs.get('priority')
        if priority is not None:
            task.priority = priority

        expiration_date = kwargs.get('expiration_date')
        if expiration_date is not None:
            task.expiration_date = expiration_date

        self.save()

    @log_func
    def edit_project(self, new_name):
        self._project.name = new_name
        self.save()

    @log_func
    def free_tasks_list(self, task_list_id):
        task_list = self.get_task_list_by_id(task_list_id)
        self._tasks = [task for task in self._tasks if
                       task.unique_id not in task_list.tasks_list]
        task_list.tasks_list.clear()
        self.save()

    @log_func
    def get_tasks(self, task_list_id=None):
        if task_list_id is None:
            return self._tasks
        else:
            task_list = self.get_task_list_by_id(task_list_id)
            if task_list is not None:
                return [task for task in self._tasks if
                        task.unique_id in task_list.tasks_list]
            return None

    @log_func
    def get_task_lists(self):
        return self._task_lists

    @log_func
    def get_task_by_id(self, task_id):
        if task_id is None:
            return None
        return find_one(self._tasks, task_id)

    @log_func
    def get_task_list_by_id(self, task_list_id):
        if task_list_id is None:
            return None
        return find_one(self._task_lists, task_list_id)

    @log_func
    def get_plans(self):
        return self._plans

    @log_func
    def get_plan_by_id(self, plan_id):
        if plan_id is None:
            return None
        return find_one(self._plans, plan_id)

    # endregion
