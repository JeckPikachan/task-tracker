#! /usr/bin/python3.6

# from app.app import App
#
# app = App()
#
# # app.add_list('some test task list')
# app.change_task_list_name('70ee354d-a325-405e-98fd-7c09ea53fd56', 'The To Do task list')
# app.add_task('ea4a6c5a-488b-478e-a0c9-1ea58b3c77f3', 'Do Labs')
# task_lists = app.get_task_lists()
# for task_list in task_lists:
#     print(task_list.name + "\t: " + task_list.unique_id)
#
# tasks = app.get_tasks('70ee354d-a325-405e-98fd-7c09ea53fd56')
# tasks = [{'unique_id': task.unique_id, 'name': task.name} for task in tasks]
# print(tasks)
# # task = Task(name="name")
import os

from app import App
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

    if args.command == 'show':
        if args.kind == 'project':
            project = app.get_project()
            if args.all:
                projects = app.get_projects()
                print_projects(projects, project.unique_id)
            else:
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

    if args.command == 'checkout':
        app.load_project(args.project_id)


if __name__ == "__main__":
    main()

