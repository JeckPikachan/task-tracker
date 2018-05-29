ADD_COMMAND = {'project': lambda app, args: add_project(app, args),
               'list': lambda app, args: add_list(app, args),
               'task': lambda app, args: add_task(app, args),
               'user': lambda app, args: add_user(app, args),
               'upr': lambda app, args: add_upr(app, args),
               'relation': lambda app, args: add_relation(app, args),
               'plan': lambda app, args: add_plan(app, args)}


def add_project(app, args):
    app.add_project(args.name)


def add_list(app, args):
    app.add_list(args.name)


def add_task(app, args):
    app.add_task(args.list_id,
                 args.name,
                 description=args.description,
                 status=args.status,
                 priority=args.priority)


def add_user(app, args):
    app.add_user(args.name)


def add_upr(app, args):
    app.add_upr(args.user_id, args.project_id)


def add_relation(app, args):
    app.add_relation(args.from_id, args.to_id, args.description)


def add_plan(app, args):
    app.add_plan(name=args.name,
                 task_list_id=args.list_id,
                 delta=args.delta,
                 status=args.status,
                 priority=args.priority,
                 description=args.description,
                 start_date=args.start_date,
                 end_date=args.end_date)
