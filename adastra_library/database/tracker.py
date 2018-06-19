import json
import os
from datetime import datetime
from json import JSONDecodeError

from adastra_library import Project, TaskList, Task, TaskPattern, PlanManager, User, UPRCollection
from database import serialization
from library_util.enum_json import deserialize_enum
from library_util.files import create_file_if_not_exists
from library_util.find import find_one_in_dicts, find_one
from library_util.log import log_func, LIBRARY_LOGGER_NAME


class TrackerData:
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


class TrackerDAO:

    def __init__(self, connection_string=None):
        self._db_path = (os.path.dirname(connection_string) + "/" if
                         connection_string is not None else
                         os.path.dirname(__file__) + "/data/")

        self._project = None
        self._task_lists = []
        self._tasks = []
        self._plans = []

    @property
    def project(self):
        return self._project

    def get_tracker_data(self):
        try:
            create_file_if_not_exists(self._db_path, "db_info.json")
            with open(self._db_path + "db_info.json", "r") as config_file:
                tracker_data = TrackerData(**json.load(config_file))
        except BaseException:
            tracker_data = TrackerData()
        return tracker_data

    def save_tracker_data(self, tracker_data):
        try:
            create_file_if_not_exists(self._db_path,
                                      "db_info.json")
            with open(self._db_path + "db_info.json", "w+") as config_file:
                json.dump(serialization.transform_object(tracker_data),
                          config_file, indent=4)
            return None
        except IOError as e:
            return e

    def load_project_from_file(self, project_id):
        try:
            create_file_if_not_exists(self._db_path + "projects/",
                                      project_id + ".json")
            with open(self._db_path + "projects/" + project_id + ".json", "r") as \
                    project_file:
                loaded = json.load(project_file)
                project = loaded.get('project')
                lists = loaded.get('task_lists', [])
                tasks = loaded.get('tasks', [])
                for task in tasks:
                    task['status'] = deserialize_enum(task['status'])
                    task['priority'] = deserialize_enum(task['priority'])
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

                    plans.append(
                        PlanManager(
                            delta=plan.get('delta', None),
                            task_list_id=plan.get('task_list_id', None),
                            task_pattern=plan.get('task_pattern', None),
                            start_date=plan.get('start_date', None),
                            end_date=plan.get('end_date', None),
                            last_created=plan.get('last_created', None),
                            unique_id=plan.get('unique_id', None)
                        )
                    )

                self._plans = plans

                current_project_id = project.get('unique_id')
            return current_project_id
        except IOError as e:
            raise e

    def load_project(self, tracker_data, project_id=None):
        if project_id is None:
            current_project_id = tracker_data.current_project_id

            if current_project_id is not None:
                self.load_project_from_file(current_project_id)

        else:
            new_current_project_id = self.load_project_from_file(project_id)
            return new_current_project_id

    def load_uprs(self):
        try:
            create_file_if_not_exists(self._db_path + "uprs/",
                                      "uprs.json")
            with open(self._db_path + "uprs/uprs.json", "r") as uprs_file:
                loaded = json.load(uprs_file)
                uprs_collection = UPRCollection(**loaded)
        except IOError as e:
            raise e
        except JSONDecodeError as e:
            uprs_collection = UPRCollection()
        return uprs_collection

    def load_user(self, user_id):
        try:
            create_file_if_not_exists(self._db_path + "users/",
                                      user_id + ".json")
            with open(self._db_path + "users/" + user_id + ".json", "r") as user_file:
                loaded = json.load(user_file)
                user = User(**loaded)
            return user
        except IOError as e:
            raise e

    def save_project(self):
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
            create_file_if_not_exists(self._db_path + "projects/",
                                      project_id + ".json")
            with open(self._db_path + "projects/" + project_id + ".json", "w+") as \
                    project_file:
                json.dump(dict_to_save, project_file, indent=4)
        except IOError:
            raise

        return project_name, project_id

    def save_user(self, user):
        try:
            create_file_if_not_exists(self._db_path + "users/",
                                      user.unique_id + ".json")
            with open(self._db_path + "users/" + user.unique_id + ".json", "w+") as \
                    user_file:
                json.dump(serialization.transform_object(user), user_file, indent=4)
            return None
        except IOError as e:
            return e

    def save_uprs(self, uprs_collection):
        try:
            create_file_if_not_exists(self._db_path + "uprs/",
                                      "uprs.json")
            with open(self._db_path + "uprs/uprs.json", "w+") as uprs_file:
                json.dump(serialization.transform_upr_collection(uprs_collection),
                          uprs_file, indent=4)
            return None
        except IOError as e:
            return e

    def remove_project(self, project_id):
        try:
            os.remove(self._db_path + "projects/" + project_id + ".json")
        except OSError:
            pass

    def add_project(self, project):
        dict_to_save = {'project': serialization.transform_project(project)}
        project_id = project.unique_id

        try:
            create_file_if_not_exists(self._db_path + "projects/",
                                      project_id + ".json")
            with open(self._db_path + "projects/" + project_id + ".json", "w+") as \
                    project_file:
                json.dump(dict_to_save, project_file, indent=4)

        except IOError:
            raise

    def add_list(self, task_list):
        self._task_lists.append(task_list)
        self._project.lists.append(task_list.unique_id)
        self.save_project()

    def get_task_list_by_id(self, task_list_id):
        if task_list_id is None:
            return None
        return find_one(self._task_lists, task_list_id)

    def free_tasks_list(self, task_list_id):
        task_list = self.get_task_list_by_id(task_list_id)
        self._tasks = [task for task in self._tasks if
                       task.unique_id not in task_list.tasks_list]
        task_list.tasks_list.clear()
        self.save_project()

    def remove_list(self, task_list_id):
        self.free_tasks_list(task_list_id)
        self._project.lists.remove(task_list_id)
        self._task_lists = [task_list for task_list in self._task_lists if
                            task_list.unique_id != task_list_id]
        self.save_project()

    def add_task(self, task_list_id, task):
        task_list = self.get_task_list_by_id(task_list_id)
        if task_list is not None:
            self._tasks.append(task)
            task_list.tasks_list.append(task.unique_id)
        else:
            raise ValueError("No task list with such id")
        self.save_project()

    def remove_task(self, task_id):
        for task_list in self._task_lists:
            if task_id in task_list.tasks_list:
                task_list.tasks_list.remove(task_id)
        self._tasks = [task for task in self._tasks if
                       task.unique_id != task_id]
        self.save_project()

    def get_task_by_id(self, task_id):
        if task_id is None:
            return None
        return find_one(self._tasks, task_id)

    def add_relation(self, from_id, to_id, description=None):
        from_task = self.get_task_by_id(from_id)
        to_task = self.get_task_by_id(to_id)
        if from_task is None or to_task is None:
            raise NameError("No task(s) with such id")
        if to_task.unique_id in [x.to for x in from_task.related_tasks_list]:
            raise NameError("Such relation already exists")
        new_relation = from_task.add_relation(to_id, description)
        self.save_project()
        return new_relation

    def remove_relation(self, from_id, to_id):
        from_task = self.get_task_by_id(from_id)
        if from_task is None:
            raise NameError("No task with such id")
        from_task.remove_relation(to_id)
        self.save_project()

    def add_plan(self, task_list_id, plan):
        task_list = self.get_task_list_by_id(task_list_id)
        if task_list is not None:
            self._plans.append(plan)
        else:
            raise ValueError("No task list with such id")
        self.save_project()

    def remove_plan(self, plan_id):
        self._plans = [plan for plan in
                       self._plans if plan.unique_id != plan_id]
        self.save_project()

    def edit_list(self, task_list_id, new_name):
        task_list = self.get_task_list_by_id(task_list_id)
        if task_list is not None and new_name is not None:
            task_list.name = new_name
        self.save_project()

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

        self.save_project()

    def edit_project(self, new_name):
        self._project.name = new_name
        self.save_project()

    def get_tasks(self, task_list_id=None):
        if task_list_id is None:
            return self._tasks
        else:
            task_list = self.get_task_list_by_id(task_list_id)
            if task_list is not None:
                return [task for task in self._tasks if
                        task.unique_id in task_list.tasks_list]
            return None

    def get_task_lists(self):
        return self._task_lists

    def get_plans(self):
        return self._plans

    def get_plan_by_id(self, plan_id):
        if plan_id is None:
            return None
        return find_one(self._plans, plan_id)


class Tracker:
    """

    Tracker class is used to manage simple json data base
    and to encapsulate operations on json files.
    """

    # region magic methods

    def __init__(self, tracker_dao):
        self.tracker_dao = tracker_dao
        self.tracker_data = self.tracker_dao.get_tracker_data()

    # endregion
    # region load methods

    @log_func(LIBRARY_LOGGER_NAME)
    def load_project(self, project_id=None):
        new_current_project_id = \
            self.tracker_dao.load_project(
                self.tracker_data,
                project_id
            )
        self.tracker_data.current_project_id = new_current_project_id
        if new_current_project_id is not None:
            self.tracker_dao.save_tracker_data(self.tracker_data)

    @log_func(LIBRARY_LOGGER_NAME)
    def get_user(self, user_id=None):
        if user_id is None:
            user_id = self.tracker_data.current_user_id
            if user_id is None:
                return None
        user = self.tracker_dao.load_user(user_id)
        self.tracker_data.current_user_id = user_id
        self.tracker_dao.save_tracker_data(self.tracker_data)
        return user

    @log_func(LIBRARY_LOGGER_NAME)
    def get_uprs(self):
        return self.tracker_dao.load_uprs()

    # endregion
    # region save methods

    @log_func(LIBRARY_LOGGER_NAME)
    def save_project(self):
        project_name, project_id = self.tracker_dao.save_project()

        self.tracker_data.add_project_info(project_name, project_id)
        self.tracker_dao.save_tracker_data(self.tracker_data)

    @log_func(LIBRARY_LOGGER_NAME)
    def save_user(self, user):
        self.tracker_dao.save_user(user)
        self.tracker_data.add_user_info(user.name, user.unique_id)
        self.tracker_dao.save_tracker_data(self.tracker_data)

    @log_func(LIBRARY_LOGGER_NAME)
    def save_uprs(self, uprs_collection):
        self.tracker_dao.save_uprs(uprs_collection)

    # endregion
    # region remove methods

    @log_func(LIBRARY_LOGGER_NAME)
    def remove_project(self, project_id):
        self.tracker_dao.remove_project(project_id)

        self.tracker_data.projects_info = \
            [project_info for project_info in
             self.tracker_data.projects_info if
             project_info.get('unique_id') != project_id]
        if self.tracker_data.current_project_id == project_id:
            self.tracker_data.current_project_id = None
        self.tracker_dao.save_tracker_data(self.tracker_data)

    # endregion
    # region get methods

    @log_func(LIBRARY_LOGGER_NAME)
    def get_projects_info(self):
        return (self.tracker_data.projects_info,
                self.tracker_data.current_project_id)

    def get_current_project(self):
        if self.tracker_dao.project:
            return self.tracker_dao.project
        else:
            raise AttributeError("Project not chosen or doesn't exist!")

    @log_func(LIBRARY_LOGGER_NAME)
    def get_users_info(self):
        return (self.tracker_data.users_info,
                self.tracker_data.current_user_id)

    # endregion
    # region change methods

    @log_func(LIBRARY_LOGGER_NAME)
    def leave_project(self):
        self.tracker_data.current_project_id = None
        self.tracker_dao.save_tracker_data(self.tracker_data)

    # endregion
    # region API

    @log_func(LIBRARY_LOGGER_NAME)
    def add_project(self, project):
        self.tracker_dao.add_project(project)

        project_id = project.unique_id
        project_name = project.name

        self.tracker_data.add_project_info(project_name, project_id)
        self.tracker_dao.save_tracker_data(self.tracker_data)

    @log_func(LIBRARY_LOGGER_NAME)
    def add_list(self, task_list):
        self.tracker_dao.add_list(task_list)

    @log_func(LIBRARY_LOGGER_NAME)
    def remove_list(self, task_list_id):
        self.tracker_dao.remove_list(task_list_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def add_task(self, task_list_id, task):
        self.tracker_dao.add_task(task_list_id, task)

    @log_func(LIBRARY_LOGGER_NAME)
    def remove_task(self, task_id):
        self.tracker_dao.remove_task(task_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def add_relation(self, from_id, to_id, description=None):
        return self.tracker_dao.add_relation(from_id, to_id, description)

    @log_func(LIBRARY_LOGGER_NAME)
    def remove_relation(self, from_id, to_id):
        self.tracker_dao.remove_relation(from_id, to_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def add_plan(self, task_list_id, plan):
        self.tracker_dao.add_plan(task_list_id, plan)

    @log_func(LIBRARY_LOGGER_NAME)
    def remove_plan(self, plan_id):
        self.tracker_dao.remove_plan(plan_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def edit_list(self, task_list_id, new_name):
        self.tracker_dao.edit_list(task_list_id, new_name)

    @log_func(LIBRARY_LOGGER_NAME)
    def edit_task(self, task_id, **kwargs):
        self.tracker_dao.edit_task(task_id, **kwargs)

    @log_func(LIBRARY_LOGGER_NAME)
    def edit_project(self, new_name):
        self.tracker_dao.edit_project(new_name)

    @log_func(LIBRARY_LOGGER_NAME)
    def free_tasks_list(self, task_list_id):
        self.tracker_dao.free_tasks_list(task_list_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def get_tasks(self, task_list_id=None):
        return self.tracker_dao.get_tasks(task_list_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def get_task_lists(self):
        return self.tracker_dao.get_task_lists()

    @log_func(LIBRARY_LOGGER_NAME)
    def get_task_by_id(self, task_id):
        return self.tracker_dao.get_task_by_id(task_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def get_task_list_by_id(self, task_list_id):
        return self.tracker_dao.get_task_list_by_id(task_list_id)

    @log_func(LIBRARY_LOGGER_NAME)
    def get_plans(self):
        return self.tracker_dao.get_plans()

    @log_func(LIBRARY_LOGGER_NAME)
    def get_plan_by_id(self, plan_id):
        return self.tracker_dao.get_plan_by_id(plan_id)

    # endregion
