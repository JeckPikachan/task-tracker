import datetime

from adastra_library import UniqueObject
from library_util import delta_time


def print_unique_object(obj):
    if not isinstance(obj, UniqueObject):
        print()
        return
    print("* name : " + str(obj.name))
    print("  id   : " + str(obj.unique_id))


def print_unique_objects(objs):
    for obj in objs:
        print_unique_object(obj)


def print_tasks(tasks, verbose=False):
    for task in tasks:
        print_unique_object(task)
        if verbose:
            print("description: " + str(task.description))
            print("expiration date: " + str(task.expiration_date))
            print("status: " + str(task.status))
            print("priority: " + str(task.priority))
        print()


def print_projects(projects, current_project_id):
    for project in projects:
        if current_project_id == project.get('unique_id'):
            print("(CURRENT)")
        print("name: " + project.get('name'))
        print("id: " + project.get('unique_id'))
        print()


def print_users(users, current_user_id):
    for user in users:
        if current_user_id == user.get('unique_id'):
            print("(CURRENT)")
        print("name: " + user.get('name'))
        print("id: " + user.get('unique_id'))
        print()


def get_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp) if\
        timestamp is not None else None


def get_delta(delta):
    deltas = {delta_time.DAILY: "DAILY",
              delta_time.WEEKLY: "WEEKLY",
              delta_time.MONTHLY: "MONTHLY",
              delta_time.YEARLY: "YEARLY"}
    return deltas.get(delta, None)


def print_pattern(task_pattern, indent):
    spaces = " " * indent
    print("{0}name        : {1}".format(spaces, task_pattern.name))
    print("{0}description : {1}".format(spaces, task_pattern.description))
    print("{0}priority    : {1}".format(spaces, task_pattern.priority))
    print("{0}status      : {1}".format(spaces, task_pattern.status))
    print("{0}author id   : {1}".format(spaces, task_pattern.author))


def print_plan(plan):
    print("* plan id    : {}".format(plan.unique_id))
    print("  list id    : {}".format(plan.task_list_id))
    print("  start date : {}".format(plan.start_date))
    print("  end date   : {}".format(plan.end_date))
    print("  last       : {}".format(plan.last_created))
    print("  delta      : {}".format(get_delta(plan.delta)))
    print("  pattern    : ")
    print_pattern(plan.task_pattern, 8)


def print_plans(plans):
    for plan in plans:
        print_plan(plan)
        print()



