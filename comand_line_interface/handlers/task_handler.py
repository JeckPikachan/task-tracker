from library_util.find import find_one


ACTIONS = {
    'add': lambda app, args: add_task(app, args),
    'edit': lambda app, args: edit_task(app, args),
    'remove': lambda app, args: remove_task(app, args),
    'show': lambda app, args: show_task(app, args),
}


def add_task(app, args):
    app.add_task(args.list_id,
                 args.name,
                 description=args.description,
                 status=args.status,
                 priority=args.priority)


def edit_task(app, args):
    app.edit_task(**args.__dict__)


def remove_task(app, args):
    if args.id is not None:
        app.remove_task(args.id)
    elif args.list is not None:
        app.free_tasks_list(args.list)


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

