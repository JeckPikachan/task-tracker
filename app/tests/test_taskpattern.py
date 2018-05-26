import unittest

from app.model.adastra_library.taskpattern import TaskPattern

NAME = "SOME NAME"
DESCRIPTION = "ANY DESCRIPTION"
ID = "ID1234567890"
STATUS = 0
PRIORITY = 2


class TestTaskPattern(unittest.TestCase):
    def setUp(self):
        self.task_pattern = TaskPattern(NAME, DESCRIPTION, PRIORITY, STATUS, ID)

    def tearDown(self):
        self.task_pattern = None

    def test_name(self):
        self.assertEqual(self.task_pattern.name, NAME)

    def test_description(self):
        self.assertEqual(self.task_pattern.description, DESCRIPTION)

    def test_status(self):
        self.assertEqual(self.task_pattern.status, STATUS)

    def test_priority(self):
        self.assertEqual(self.task_pattern.priority, PRIORITY)

    def test_author(self):
        self.assertEqual(self.task_pattern.author, ID)

    def test_get_task_create_params(self):
        params = {
            "name": NAME,
            "description": DESCRIPTION,
            "priority": PRIORITY,
            "status": STATUS,
            "author": ID
        }
        self.assertEqual(self.task_pattern.get_task_create_params(), params)
