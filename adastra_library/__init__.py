r"""
Adastra library is designed to be used as Task tracker.
It contains all needed classes. You only have to create your own
interface. It can be whatever you want: console, web or any other.
Library logs its info to logger with name 'adastra_library', so
you can override its settings.
"""
from .adastra_library import *
from .database import *


__version__ = '0.0.1'
__all__ = [
    'Task', 'TaskList', 'PlanManager', 'Project', 'ProjectContainer',
    'TaskPattern', 'TaskRelation', 'Status', 'Priority', 'UPRCollection',
    'User', 'UserProjectRelation', 'DataBase', 'DBInfo'
]

__author__ = 'Eugene Kachanovski'

