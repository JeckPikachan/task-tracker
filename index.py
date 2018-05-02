#! /usr/bin/python3.6

import os

from app import App, NoContainerError
from user_interface.parser import Parser


def print_unique_object(obj):
    print("name: " + str(obj.name))
    print("id: " + str(obj.unique_id))


def print_unique_objects(objs):
    for obj in objs:
        print_unique_object(obj)


def print_task_lists(task_lists, verbose=False):
    for task_list in task_lists:
        print_unique_object(task_list)
        if verbose:
            print("tasks: ", task_list.tasks_list)
        print()


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


def main():
    app = App(str(os.getcwd()) + '/app/')
    parser = Parser()
    args = parser.parse()

    try:
        if args.command == 'show':
            if args.kind == 'project':

                if args.all:
                    projects = app.get_projects_info()
                    print_projects(projects.projects_info, projects.current_project_id)
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

                print_task_lists(lists, verbose)

            if args.kind == 'task':
                list_id = args.list
                tasks = app.get_tasks(list_id)
                verbose = args.verbose

                if args.title is not None:
                    tasks = [task for task in tasks if task.name == args.title]
                elif args.id is not None:
                    tasks = [next((x for x in tasks if x.unique_id == args.id), None)]

                print_tasks(tasks, verbose)

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

        if args.command == 'checkout':
            app.load_project(args.project_id)

    except NoContainerError as e:
        print(e.message)

if __name__ == "__main__":
    main()

