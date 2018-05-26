import unittest

import time

from app.model.planmanager import PlanManager
from app.model.taskpattern import TaskPattern
from app.util.deltatime import get_time_from_delta
from app.model.task import Priority, Status

DELTA = get_time_from_delta(2)
NAME = "Name"
DESCRIPTION = "Description"
STATUS = 2
PRIORITY = 2
ID = "ID1234567890"
TASK_PATTERN = TaskPattern(name=NAME,
                           description=DESCRIPTION,
                           status=STATUS,
                           priority=PRIORITY,
                           author=ID)
TASK_LIST_ID = "ID0987654321"


class TestPlanManager(unittest.TestCase):
    def setUp(self):
        self.plan = PlanManager(DELTA,
                                TASK_PATTERN,
                                TASK_LIST_ID)

    def tearDown(self):
        self.plan = None

    def test_delta(self):
        self.assertEqual(self.plan.delta, DELTA)

    def test_task_pattern(self):
        self.assertEqual(self.plan.task_pattern, TASK_PATTERN)

    def test_task_list_id(self):
        self.assertEqual(self.plan.task_list_id, TASK_LIST_ID)

    def test_get_planned_tasks(self):
        delta = DELTA
        n = 3
        current_time = time.time() + n * delta
        tasks, task_list_id = self.plan.get_planned_tasks(current_time)
        self.assertEqual(task_list_id, TASK_LIST_ID)
        self.assertEqual(len(tasks), n)
        for task in tasks:
            self.assertEqual(task.name, NAME),
            self.assertEqual(task.description, DESCRIPTION)
            self.assertEqual(task.priority, Priority.get_by_number(PRIORITY))
            self.assertEqual(task.status, Status.get_by_number(STATUS))
            self.assertEqual(task.author, ID)
