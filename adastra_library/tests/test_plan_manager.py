import unittest
from datetime import datetime

from adastra_library import Priority
from adastra_library import Status
from adastra_library.adastra_library.plan_manager import PlanManager
from adastra_library.adastra_library.task_pattern import TaskPattern
from dateutil.relativedelta import relativedelta
from library_util import delta_time

DELTA = delta_time.MONTHLY
NAME = "Name"
DESCRIPTION = "Description"
STATUS_DONE = 2
PRIORITY_HIGH = 2
ID = "ID1234567890"
TASK_PATTERN = TaskPattern(name=NAME,
                           description=DESCRIPTION,
                           status=STATUS_DONE,
                           priority=PRIORITY_HIGH,
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
        n = 3
        current_time = datetime.now() + relativedelta(months=+n)
        tasks, task_list_id = self.plan.get_planned_tasks(current_time)
        self.assertEqual(task_list_id, TASK_LIST_ID)
        self.assertEqual(len(tasks), n)
        for task in tasks:
            self.assertEqual(task.name, NAME),
            self.assertEqual(task.description, DESCRIPTION)
            self.assertEqual(task.priority, Priority.get_by_number(PRIORITY_HIGH))
            self.assertEqual(task.status, Status.get_by_number(STATUS_DONE))
            self.assertEqual(task.author, ID)
