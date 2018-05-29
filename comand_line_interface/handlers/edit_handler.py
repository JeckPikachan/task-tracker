EDIT_COMMAND = {'project': lambda app, args: edit_project(app, args),
                'list': lambda app, args: edit_list(app, args),
                'task': lambda app, args: edit_task(app, args)}


def edit_project(app, args):
    app.edit_project(args.name)


def edit_list(app, args):
    app.edit_task_list(args.list_id, args.name)


def edit_task(app, args):
    app.edit_task(**args.__dict__)
