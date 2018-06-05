import datetime

from adastra_library import UniqueObject
from library_util import delta_time
from library_util.find import find_one

SHOW_COMMAND = {'project': lambda app, args: show_project(app, args),
                'list': lambda app, args: show_list(app, args),
                'task': lambda app, args: show_task(app, args),
                'user': lambda app, args: show_user(app, args),
                'plan': lambda app, args: show_plan(app, args)}


def show_project(app, args):
    if args.all:
        projects_info, current_project_id = app.get_projects_info()
        print_projects(projects_info, current_project_id)
    else:
        project = app.get_current_project()
        print("name: " + str(project.name))
        print("id: " + str(project.unique_id))
        if args.verbose:
            print("lists: " + str(project.lists))


def show_list(app, args):
    lists = app.get_task_lists()
    verbose = args.verbose

    if args.title is not None:
        lists = [task_list for task_list in lists if task_list.name == args.title]
    elif args.id is not None:
        lists = find_one(lists, args.id)

    for task_list in lists:
        tasks = app.get_tasks(task_list.unique_id)
        print("* name : " + task_list.name)
        print("  id   : " + task_list.unique_id)
        if verbose:
            print("  tasks:")
            for task in tasks:
                print("    * name : " + task.name)
                print("      id   : " + task.unique_id)
        print()


def show_task(app, args):
    list_id = args.list
    tasks = app.get_tasks(list_id)
    verbose = args.verbose

    if args.title is not None:
        tasks = [task for task in tasks if task.name == args.title]
    elif args.id is not None:
        tasks = [find_one(tasks, args.id)]

    for task in tasks:
        related_tasks = [app.get_task_by_id(x.to) for x in task.related_tasks_list]
        print("* name            : " + task.name)
        print("  id              : " + task.unique_id)
        if verbose:
            print("  description     : " + str(task.description))
            print("  expiration date : " + str(task.expiration_date))
            print("  status          : " + str(task.status))
            print("  priority        : " + str(task.priority))
            if related_tasks:
                print("  related tasks   :")
                for i in range(len(related_tasks)):
                    print("        * name            : " + related_tasks[i].name)
                    print("          id              : " + related_tasks[i].unique_id)
                    print("          relation        : " + task.related_tasks_list[i].description)

        print()


def show_user(app, args):
    if args.all:
        users_info, current_user_id = app.get_users_info()
        print_users(users_info, current_user_id)
    else:
        user = app.get_user()
        print("name: " + str(user.name))
        print("id: " + str(user.unique_id))


def show_plan(app, args):
    if args.id is not None:
        plan = app.get_plan_by_id(args.id)
        print_plan(plan)
    else:
        plans = app.get_plans()
        print_plans(plans)


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



