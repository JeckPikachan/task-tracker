import unittest

from app.model.adastra_library.tasklist import TaskList

NAME = "Some name"


class TestTaskList(unittest.TestCase):
    def setUp(self):
        self.task_list = TaskList(name=NAME)

    def tearDown(self):
        self.task_list = None

    def test_name(self):
        self.assertEqual(self.task_list.name, NAME)

    def test_unique_id(self):
        self.assertIsInstance(self.task_list.unique_id, str)

    def test_tasks_list(self):
        self.assertListEqual(self.task_list.tasks_list, [])
