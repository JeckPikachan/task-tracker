import unittest

from adastra_library.models.task_pattern import TaskPattern

NAME = "SOME NAME"
DESCRIPTION = "ANY DESCRIPTION"
ID = "ID1234567890"
STATUS_CREATED = 0
PRIORITY_HIGH = 2


class TestTaskPattern(unittest.TestCase):
    def setUp(self):
        self.task_pattern = TaskPattern(NAME, DESCRIPTION, PRIORITY_HIGH, STATUS_CREATED, ID)

    def tearDown(self):
        self.task_pattern = None

    def test_name(self):
        self.assertEqual(self.task_pattern.name, NAME)

    def test_description(self):
        self.assertEqual(self.task_pattern.description, DESCRIPTION)

    def test_status(self):
        self.assertEqual(self.task_pattern.status, STATUS_CREATED)

    def test_priority(self):
        self.assertEqual(self.task_pattern.priority, PRIORITY_HIGH)

    def test_author(self):
        self.assertEqual(self.task_pattern.author, ID)

    def test_get_task_create_params(self):
        params = {
            "name": NAME,
            "description": DESCRIPTION,
            "priority": PRIORITY_HIGH,
            "status": STATUS_CREATED,
            "author": ID
        }
        self.assertEqual(self.task_pattern.get_task_create_params(), params)
