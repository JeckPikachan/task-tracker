#! /usr/bin/python3.6
import datetime

from app import App, NoContainerError
from app.util.deltatime import get_delta_from_time
from user_interface.parser import Parser


def print_unique_object(obj):
    if obj is None:
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


def get_delta(timestamp):
    delta = get_delta_from_time(timestamp)
    deltas = {0: "DAILY", 1: "WEEKLY", 2: "MONTHLY", 3: "YEARLY"}
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
    print("  start date : {}".format(get_date(plan.start_date)))
    print("  end date   : {}".format(get_date(plan.end_date)))
    print("  last       : {}".format(get_date(plan.last_created)))
    print("  delta      : {}".format(get_delta(plan.delta)))
    print("  pattern    : ")
    print_pattern(plan.task_pattern, 8)


def print_plans(plans):
    for plan in plans:
        print_plan(plan)
        print()


def main():
    """
    Entry point of Adastra Task Tracker.
    UI is represented by CLI.

    :return:
    """

    app = App()
    parser = Parser()
    args = parser.parse()

    try:
        if args.command == 'show':
            if args.kind == 'project':

                if args.all:
                    projects_info, current_project_id = app.get_projects_info()
                    print_projects(projects_info, current_project_id)
                else:
                    project = app.get_project()
                    print("name: " + str(project.name))
                    print("id: " + str(project.unique_id))
                    if args.verbose:
                        print("lists: " + str(project.lists))

            if args.kind == 'list':
                lists = app.get_task_lists()
                verbose = args.verbose

                if args.title is not None:
                    lists = [task_list for task_list in lists if task_list.name == args.title]
                elif args.id is not None:
                    lists = [next((x for x in lists if x.unique_id == args.id), None)]

                for list in lists:
                    tasks = app.get_tasks(list.unique_id)
                    print("* name : " + list.name)
                    print("  id   : " + list.unique_id)
                    if verbose:
                        print("  tasks:")
                        for task in tasks:
                            print("    * name : " + task.name)
                            print("      id   : " + task.unique_id)
                    print()

            if args.kind == 'task':
                list_id = args.list
                tasks = app.get_tasks(list_id)
                verbose = args.verbose

                if args.title is not None:
                    tasks = [task for task in tasks if task.name == args.title]
                elif args.id is not None:
                    tasks = [next((x for x in tasks if x.unique_id == args.id), None)]

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

            if args.kind == 'user':
                if args.all:
                    users_info, current_user_id = app.get_users_info()
                    print_users(users_info, current_user_id)
                else:
                    user = app.get_user()
                    print("name: " + str(user.name))
                    print("id: " + str(user.unique_id))

            if args.kind == 'plan':
                if args.id is not None:
                    plan = app.get_plan_by_id(args.id)

                else:
                    plans = app.get_plans()
                    print_plans(plans)

        if args.command == 'add':
            if args.kind == 'project':
                app.add_project(args.name)

            elif args.kind == 'list':
                app.add_list(args.name)

            elif args.kind == 'task':
                app.add_task(args.list_id,
                             args.name,
                             description=args.description,
                             status=args.status,
                             priority=args.priority)

            elif args.kind == 'user':
                app.add_user(args.name)

            elif args.kind == 'upr':
                app.add_upr(args.user_id, args.project_id)

            elif args.kind == 'relation':
                app.add_relation(args.from_id, args.to_id, args.description)

            elif args.kind == 'plan':
                app.add_plan(name=args.name,
                             task_list_id=args.list_id,
                             delta=args.delta,
                             status=args.status,
                             priority=args.priority,
                             description=args.description,
                             start_date=args.start_date,
                             end_date=args.end_date)

        if args.command == 'remove':
            if args.kind == 'task':
                if args.id is not None:
                    app.remove_task(args.id)
                elif args.list is not None:
                    app.free_tasks_list(args.list)

            if args.kind == 'list':
                app.remove_list(args.list_id)

            if args.kind == 'project':
                app.remove_project(args.project_id)

            if args.kind == 'upr':
                app.remove_upr(args.user_id, args.project_id)

            if args.kind == 'relation':
                app.remove_relation(args.from_id, args.to_id)

            if args.kind == 'plan':
                app.remove_plan(args.plan_id)

        if args.command == 'edit':
            if args.kind == 'project':
                app.edit_project(args.name)

            if args.kind == 'list':
                app.edit_task_list(args.list_id, args.name)

            if args.kind == 'task':
                app.edit_task(**args.__dict__)

        if args.command == 'checkout':
            app.load_project(args.project_id)

        if args.command == 'chuser':
            app.change_user(args.user_id)

    except NoContainerError as e:
        print(e.message)


if __name__ == "__main__":
    main()

