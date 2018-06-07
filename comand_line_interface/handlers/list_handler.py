from library_util.find import find_one


ACTIONS = {
    'add': lambda app, args: add_list(app, args),
    'edit': lambda app, args: edit_list(app, args),
    'remove': lambda app, args: remove_list(app, args),
    'show': lambda app, args: show_list(app, args),
}


def add_list(app, args):
    app.add_list(args.name)


def edit_list(app, args):
    app.edit_task_list(args.list_id, args.name)


def remove_list(app, args):
    app.remove_list(args.list_id)


def show_list(app, args):
    lists = app.get_task_lists()
    verbose = args.verbose

    if args.title is not None:
        lists = [task_list for task_list in lists if task_list.name == args.title]
    elif args.id is not None:
        lists = [find_one(lists, args.id)]

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
