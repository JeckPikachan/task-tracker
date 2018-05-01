import argparse


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Issue Tracker CLI')
        self.subparsers_for_command = self.parser.add_subparsers(dest='command')

    def parse(self):
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

        parser_show_task = subparsers_for_show.add_parser('project')
        parser_show_task.add_argument('-v', '--verbose', action='store_true')

        args = self.parser.parse_args()
        return args

