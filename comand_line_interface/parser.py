import argparse
from datetime import datetime

from library_util import delta_time


def parse_valid_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M')
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


class Parser:
    """

    Parser class implements basic CLI params
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Issue Tracker CLI')
        self.object_subparsers = self.parser.add_subparsers(dest='object')
        self._add_all_parsers()

    def parse(self):
        args = self.parser.parse_args()
        return args

    def _add_all_parsers(self):
        self._add_task_parser()
        self._add_list_parser()
        self._add_project_parser()
        self._add_user_parser()
        self._add_upr_parser()
        self._add_relation_parser()
        self._add_plan_parser()
        self._add_parser_for_checkout()
        self._add_parser_for_chuser()

    def _add_task_parser(self):
        task_parser = self.object_subparsers.add_parser('task')
        task_subparsers = task_parser.add_subparsers(dest='action')

        parser_show_task = task_subparsers.add_parser('show')
        parser_show_task.add_argument('-l', '--list')
        show_task_group = parser_show_task.add_mutually_exclusive_group()
        show_task_group.add_argument('-t', '--title')
        show_task_group.add_argument('--id')
        parser_show_task.add_argument('-v', '--verbose', action='store_true')

        parser_add_task = task_subparsers.add_parser('add')
        parser_add_task.add_argument('list_id')
        parser_add_task.add_argument('name')
        parser_add_task.add_argument('-d', '--description')
        parser_add_task.add_argument('-p', '--priority', type=int, choices=[0, 1, 2],
                                     help="0 - low, 1 - middle (default), 2 - high")
        parser_add_task.add_argument('-s', '--status', type=int, choices=[0, 1, 2],
                                     help="0 - created (default), 1 - in work, 2 - done")

        parser_remove_task = task_subparsers.add_parser('remove')
        remove_task_group = parser_remove_task.add_mutually_exclusive_group(required=True)
        remove_task_group.add_argument('--id')
        remove_task_group.add_argument('-l', '--list')

        parser_edit_task = task_subparsers.add_parser('edit')
        parser_edit_task.add_argument('-n', '--name')
        parser_edit_task.add_argument('-d', '--description')
        parser_edit_task.add_argument('-p', '--priority', type=int, choices=[0, 1, 2],
                                      help="0 - low, 1 - middle (default), 2 - high")
        parser_edit_task.add_argument('-s', '--status', type=int, choices=[0, 1, 2],
                                      help="0 - created (default), 1 - in work, 2 - done")
        parser_edit_task.add_argument("-e",
                                      "--expiration_date",
                                      help="The Expiration Date - format YYYY-MM-DD hh:mm",
                                      type=parse_valid_date)
        parser_edit_task.add_argument('task_id')

    def _add_list_parser(self):
        list_parser = self.object_subparsers.add_parser('list')
        list_subparsers = list_parser.add_subparsers(dest='action')

        parser_show_list = list_subparsers.add_parser('show')
        show_task_group = parser_show_list.add_mutually_exclusive_group()
        show_task_group.add_argument('-t', '--title')
        show_task_group.add_argument('--id')
        parser_show_list.add_argument('-v', '--verbose', action='store_true')

        parser_add_list = list_subparsers.add_parser('add')
        parser_add_list.add_argument('name')

        parser_remove_list = list_subparsers.add_parser('remove')
        parser_remove_list.add_argument('list_id')

        parser_edit_list = list_subparsers.add_parser('edit')
        parser_edit_list.add_argument('-n', '--name')
        parser_edit_list.add_argument('list_id')

    def _add_project_parser(self):
        project_parser = self.object_subparsers.add_parser('project')
        project_subparsers = project_parser.add_subparsers(dest='action')

        parser_show_project = project_subparsers.add_parser('show')
        parser_show_project.add_argument('-a', '--all', action='store_true')
        parser_show_project.add_argument('-v', '--verbose', action='store_true')

        parser_add_project = project_subparsers.add_parser('add')
        parser_add_project.add_argument('name')

        parser_remove_project = project_subparsers.add_parser('remove')
        parser_remove_project.add_argument('project_id')

        parser_edit_project = project_subparsers.add_parser('edit')
        parser_edit_project.add_argument('-n', '--name')

    def _add_user_parser(self):
        user_parser = self.object_subparsers.add_parser('user')
        user_subparsers = user_parser.add_subparsers(dest='action')

        parser_show_user = user_subparsers.add_parser('show')
        parser_show_user.add_argument('-a', '--all', action='store_true')

        parser_add_user = user_subparsers.add_parser('add')
        parser_add_user.add_argument('name')

    def _add_upr_parser(self):
        upr_parser = self.object_subparsers.add_parser('upr')
        upr_subparsers = upr_parser.add_subparsers(dest='action')

        parser_add_upr = upr_subparsers.add_parser('add')
        parser_add_upr.add_argument("user_id")
        parser_add_upr.add_argument("project_id")

        parser_remove_upr = upr_subparsers.add_parser('remove')
        parser_remove_upr.add_argument('user_id')
        parser_remove_upr.add_argument('project_id')

    def _add_relation_parser(self):
        relation_parser = self.object_subparsers.add_parser('relation')
        relation_subparsers = relation_parser.add_subparsers(dest='action')

        parser_add_relation = relation_subparsers.add_parser('add')
        parser_add_relation.add_argument('-d', '--description')
        parser_add_relation.add_argument('from_id')
        parser_add_relation.add_argument('to_id')

        parser_remove_relation = relation_subparsers.add_parser('remove')
        parser_remove_relation.add_argument('from_id')
        parser_remove_relation.add_argument('to_id')

    def _add_plan_parser(self):
        plan_parser = self.object_subparsers.add_parser('plan')
        plan_subparsers = plan_parser.add_subparsers(dest='action')

        parser_show_plan = plan_subparsers.add_parser('show')
        parser_show_plan.add_argument('--id')

        parser_add_plan = plan_subparsers.add_parser('add')
        parser_add_plan.add_argument('delta', type=int,
                                     choices=[delta_time.DAILY,
                                              delta_time.WEEKLY,
                                              delta_time.MONTHLY,
                                              delta_time.YEARLY],
                                     help="0 - day, 1 - week, 2 - month, 3 - year")
        parser_add_plan.add_argument('list_id')
        parser_add_plan.add_argument('name')
        parser_add_plan.add_argument('-d', '--description')
        parser_add_plan.add_argument('-p', '--priority', type=int, choices=[0, 1, 2],
                                     help="0 - low, 1 - middle (default), 2 - high")
        parser_add_plan.add_argument('-s', '--status', type=int, choices=[0, 1, 2],
                                     help="0 - created (default), 1 - in work, 2 - done")
        parser_add_plan.add_argument("-t",
                                     "--start_date",
                                     help="Start Date - format YYYY-MM-DD hh:mm",
                                     type=parse_valid_date)
        parser_add_plan.add_argument("-e",
                                     "--end_date",
                                     help="End Date - format YYYY-MM-DD hh:mm",
                                     type=parse_valid_date)

        parser_remove_plan = plan_subparsers.add_parser('remove')
        parser_remove_plan.add_argument('plan_id')

    def _add_parser_for_checkout(self):
        parser_checkout = self.object_subparsers.add_parser('checkout')
        parser_checkout.add_argument('project_id')

    def _add_parser_for_chuser(self):
        parser_chuser = self.object_subparsers.add_parser('chuser')
        parser_chuser.add_argument('user_id')
