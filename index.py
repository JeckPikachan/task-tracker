#! /usr/bin/python3.6

from app import App, NoContainerError
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

