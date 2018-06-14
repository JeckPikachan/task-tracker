r"""
Adastra library is designed to be used as Task tracker.
It contains all needed classes. You only have to create your own
interface. It can be whatever you want: console, web or any other.
Library logs its info to logger with name 'adastra_library', so
you can override its settings.

The following block is covering the most common use cases:

DataBase object:
    DataBase object gets connection string as first argument:
    >>> db = DataBase("[path to your database]")
    Or you can leave it empty and it will use default path:
    >>> db = DataBase()

User:
    >>> new_user = User("[user name]")
    To save user use:
    >>> db.save_user(new_user)
    Getting user from database:
    >>> user = db.load_user("[user id]")

Project:
    >>> new_project = Project("[project name]")
    To save project use:
    >>> db.add_project(new_project)

TaskList:
    >>> new_task_list = TaskList("[task list name]")

Task:
    The simplest example of creating task:
    >>> new_task = Task("[task name]")
    Also you can pass some other arguments:
    >>> new_task = Task(name="Some name", description="description", expiration_date=Date("Your date"))

TaskPattern:
    >>> task_pattern = TaskPattern("[task name]", description="Some desc")

PlanManager:
    First argument is delta (use one of constants from adastra_library.library_util.delta_time).
    Second argument is TaskPattern object.
    Third is task list id.
    Others are optional.
    >>> plan = PlanManager(DAILY, task_pattern, "[task list id]")

ProjectContainer:
    ProjectContainer constructor gets database you want to use
    as its first argument:
    >>> container = ProjectContainer(db)
    By default it loads project saved as current project in database.
    To switch to another project use:
    >>> container.load("[project id]")
    Add task list:
    >>> container.add_list(task_list)
    Add task to task list with specified id:
    >>> container.add_task("[task list id]", task)

"""
from .adastra_library import *
from .database import *
from adastra_library.library_util import *


__version__ = '0.0.1'
__all__ = [
    'Task', 'TaskList', 'PlanManager', 'Project', 'ProjectContainer',
    'TaskPattern', 'TaskRelation', 'Status', 'Priority', 'UPRCollection',
    'User', 'UserProjectRelation', 'DataBase', 'DBInfo'
]

__author__ = 'Eugene Kachanovski'

