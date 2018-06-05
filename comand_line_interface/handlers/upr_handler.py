ACTIONS = {
    'add': lambda app, args: add_upr(app, args),
    'remove': lambda app, args: remove_upr(app, args),
}


def add_upr(app, args):
    app.add_upr(args.user_id, args.project_id)


def remove_upr(app, args):
    app.remove_upr(args.user_id, args.project_id)
