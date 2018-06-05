from comand_line_interface.handlers.printers import print_users


ACTIONS = {
    'add': lambda app, args: add_user(app, args),
    'show': lambda app, args: show_user(app, args),
}


def add_user(app, args):
    app.add_user(args.name)


def show_user(app, args):
    if args.all:
        users_info, current_user_id = app.get_users_info()
        print_users(users_info, current_user_id)
    else:
        user = app.get_user()
        print("name: " + str(user.name))
        print("id: " + str(user.unique_id))
