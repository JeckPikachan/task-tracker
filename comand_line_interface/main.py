#! /usr/bin/python3.6

from comand_line_interface.app import App, NoContainerError
from comand_line_interface.handlers import add_handler, edit_handler, remove_handler, show_handler
from comand_line_interface.parser import Parser


COMMANDS = {'show': lambda app, args: use_show_command(app, args),
            'add': lambda app, args: use_add_command(app, args),
            'remove': lambda app, args: use_remove_command(app, args),
            'edit': lambda app, args: use_edit_command(app, args),
            'checkout': lambda app, args: use_checkout_command(app, args),
            'chuser': lambda app, args: use_chuser_command(app, args)}


def handle_args(app, args):
    COMMANDS.get(args.command)(app, args)


def use_show_command(app, args):
    show_handler.SHOW_COMMAND.get(args.kind)(app, args)


def use_add_command(app, args):
    add_handler.ADD_COMMAND.get(args.kind)(app, args)


def use_remove_command(app, args):
    remove_handler.REMOVE_COMMAND.get(args.kind)(app, args)


def use_edit_command(app, args):
    edit_handler.EDIT_COMMAND.get(args.kind)(app, args)


def use_checkout_command(app, args):
    app.load_project(args.project_id)


def use_chuser_command(app, args):
    app.change_user(args.user_id)


def main():
    """
    Entry point of Adastra Task Tracker.
    UI is represented by CLI.

    :return:
    """

    app = App()
    parser = Parser()
    args = parser.parse()

    try:
        handle_args(app, args)
    except NoContainerError as e:
        print(e.message)
    except PermissionError as e:
        print(e.args[0])
    except Exception as e:
        print("Oops! Something went wrong!")
        print(e.args[0])


if __name__ == "__main__":
    main()

