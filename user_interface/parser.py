import argparse
from datetime import datetime


def valid_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M')
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Issue Tracker CLI')
        self.subparsers_for_command = self.parser.add_subparsers(dest='command')

    def parse(self):
        # parser for 'show' #
        parser_show = self.subparsers_for_command.add_parser('show')
        subparsers_for_show = parser_show.add_subparsers(dest='kind')

        parser_show_task = subparsers_for_show.add_parser('task')
        parser_show_task.add_argument('-l', '--list')
        show_task_group = parser_show_task.add_mutually_exclusive_group()
        show_task_group.add_argument('-t', '--title')
        show_task_group.add_argument('--id')
        parser_show_task.add_argument('-v', '--verbose', action='store_true')

        parser_show_task = subparsers_for_show.add_parser('list')
        show_task_group = parser_show_task.add_mutually_exclusive_group()
        show_task_group.add_argument('-t', '--title')
        show_task_group.add_argument('--id')
        parser_show_task.add_argument('-v', '--verbose', action='store_true')

        parser_show_project = subparsers_for_show.add_parser('project')
        parser_show_project.add_argument('-a', '--all', action='store_true')
        parser_show_project.add_argument('-v', '--verbose', action='store_true')

        parser_show_user = subparsers_for_show.add_parser('user')
        parser_show_user.add_argument('-a', '--all', action='store_true')

        # parser for 'add' #
        parser_add = self.subparsers_for_command.add_parser('add')
        subparsers_for_add = parser_add.add_subparsers(dest='kind')

        parser_add_project = subparsers_for_add.add_parser('project')
        parser_add_project.add_argument('name')

        parser_add_list = subparsers_for_add.add_parser('list')
        parser_add_list.add_argument('name')

        parser_add_task = subparsers_for_add.add_parser('task')
        parser_add_task.add_argument('list_id')
        parser_add_task.add_argument('name')
        parser_add_task.add_argument('-d', '--description')
        parser_add_task.add_argument('-p', '--priority', type=int, choices=[0, 1, 2],
                                     help="0 - low, 1 - middle (default), 2 - high")
        parser_add_task.add_argument('-s', '--status', type=int, choices=[0, 1, 2],
                                     help="0 - created (default), 1 - in work, 2 - done")

        parser_add_user = subparsers_for_add.add_parser('user')
        parser_add_user.add_argument('name')

        # parser for 'remove' #
        parser_remove = self.subparsers_for_command.add_parser('remove')
        subparsers_for_remove = parser_remove.add_subparsers(dest='kind')

        parser_remove_task = subparsers_for_remove.add_parser('task')
        remove_task_group = parser_remove_task.add_mutually_exclusive_group(required=True)
        remove_task_group.add_argument('--id')
        remove_task_group.add_argument('-l', '--list')

        parser_remove_list = subparsers_for_remove.add_parser('list')
        parser_remove_list.add_argument('list_id')

        parser_remove_project = subparsers_for_remove.add_parser('project')
        parser_remove_project.add_argument('project_id')

        # parser for 'edit' #
        parser_edit = self.subparsers_for_command.add_parser('edit')
        subparsers_for_edit = parser_edit.add_subparsers(dest='kind')

        parser_edit_project = subparsers_for_edit.add_parser('project')
        parser_edit_project.add_argument('-n', '--name')

        parser_edit_list = subparsers_for_edit.add_parser('list')
        parser_edit_list.add_argument('-n', '--name')
        parser_edit_list.add_argument('list_id')

        parser_edit_task = subparsers_for_edit.add_parser('task')
        parser_edit_task.add_argument('-n', '--name')
        parser_edit_task.add_argument('-d', '--description')
        parser_edit_task.add_argument('-p', '--priority', type=int, choices=[0, 1, 2],
                                      help="0 - low, 1 - middle (default), 2 - high")
        parser_edit_task.add_argument('-s', '--status', type=int, choices=[0, 1, 2],
                                      help="0 - created (default), 1 - in work, 2 - done")
        parser_edit_task.add_argument("-e",
                                      "--expiration_date",
                                      help="The Expiration Date - format YYYY-MM-DD hh:mm",
                                      required=True,
                                      type=valid_date)
        parser_edit_task.add_argument('task_id')

        # parser for 'checkout' #
        parser_checkout = self.subparsers_for_command.add_parser('checkout')
        parser_checkout.add_argument('project_id')

        # parser for 'chuser' #
        parser_chuser = self.subparsers_for_command.add_parser('chuser')
        parser_chuser.add_argument('user_id')

        args = self.parser.parse_args()
        return args

