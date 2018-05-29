import unittest

from adastra_library import Priority
from adastra_library import Status
from adastra_library.adastra_library.task import Task


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task()

    def tearDown(self):
        self.task = None

    def test_name(self):
        self.assertIsNone(self.task.name)

    def test_unique_id(self):
        self.assertIsInstance(self.task.unique_id, str)

    def test_description(self):
        self.assertIsNone(self.task.description)

    def test_expiration_date(self):
        self.assertIsNone(self.task.expiration_date)

    def test_priority(self):
        self.assertEqual(self.task.priority, Priority.MIDDLE)

    def test_status(self):
        self.assertEqual(self.task.status, Status.CREATED)

    def test_author(self):
        self.assertIsNone(self.task.author)

    def test_related_tasks_list(self):
        self.assertListEqual(self.task.related_tasks_list, [])

    def test_priority_assignment_int(self):
        self.task.priority = 0
        self.assertEqual(self.task.priority, Priority.LOW)

    def test_priority_assignment_enum(self):
        self.task.priority = Priority.HIGH
        self.assertEqual(self.task.priority, Priority.HIGH)

    def test_status_assignment_int(self):
        self.task.status = 2
        self.assertEqual(self.task.status, Status.DONE)

    def test_status_assignment_enum(self):
        self.task.status = Status.IN_WORK
        self.assertEqual(self.task.status, Status.IN_WORK)
