REMOVE_COMMAND = {'project': lambda app, args: remove_project(app, args),
                  'list': lambda app, args: remove_list(app, args),
                  'task': lambda app, args: remove_task(app, args),
                  'upr': lambda app, args: remove_upr(app, args),
                  'relation': lambda app, args: remove_relation(app, args),
                  'plan': lambda app, args: remove_plan(app, args)}


def remove_project(app, args):
    app.remove_project(args.project_id)


def remove_list(app, args):
    app.remove_list(args.list_id)


def remove_task(app, args):
    if args.id is not None:
        app.remove_task(args.id)
    elif args.list is not None:
        app.free_tasks_list(args.list)


def remove_upr(app, args):
    app.remove_upr(args.user_id, args.project_id)


def remove_relation(app, args):
    app.remove_relation(args.from_id, args.to_id)


def remove_plan(app, args):
    app.remove_plan(args.plan_id)
