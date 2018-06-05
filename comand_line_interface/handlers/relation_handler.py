ACTIONS = {
    'add': lambda app, args: add_relation(app, args),
    'remove': lambda app, args: remove_relation(app, args),
}


def add_relation(app, args):
    app.add_relation(args.from_id, args.to_id, args.description)


def remove_relation(app, args):
    app.remove_relation(args.from_id, args.to_id)
