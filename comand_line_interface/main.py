#! /usr/bin/python3.6

from comand_line_interface.app import App, NoContainerError
from comand_line_interface.parser import Parser
from comand_line_interface.handlers import (task_handler,
                                            plan_handler,
                                            list_handler,
                                            project_handler,
                                            relation_handler,
                                            upr_handler,
                                            user_handler)


HANDLER_MAP = {
    'task': lambda app, args: use_task_handler(app, args),
    'list': lambda app, args: use_list_handler(app, args),
    'project': lambda app, args: use_project_handler(app, args),
    'user': lambda app, args: use_user_handler(app, args),
    'upr': lambda app, args: use_upr_handler(app, args),
    'relation': lambda app, args: use_relation_handler(app, args),
    'plan': lambda app, args: use_plan_handler(app, args),
    'checkout': lambda app, args: use_checkout_handler(app, args),
    'chuser': lambda app, args: use_chuser_handler(app, args)
}


def handle_args(app, args):
    HANDLER_MAP.get(args.object)(app, args)


def use_task_handler(app, args):
    task_handler.ACTIONS.get(args.action)(app, args)


def use_list_handler(app, args):
    list_handler.ACTIONS.get(args.action)(app, args)


def use_project_handler(app, args):
    project_handler.ACTIONS.get(args.action)(app, args)


def use_user_handler(app, args):
    user_handler.ACTIONS.get(args.action)(app, args)


def use_upr_handler(app, args):
    upr_handler.ACTIONS.get(args.action)(app, args)


def use_relation_handler(app, args):
    relation_handler.ACTIONS.get(args.action)(app, args)


def use_plan_handler(app, args):
    plan_handler.ACTIONS.get(args.action)(app, args)


def use_checkout_handler(app, args):
    app.load_project(args.project_id)


def use_chuser_handler(app, args):
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

