from datetime import datetime

from dateutil.relativedelta import relativedelta

from library_util import delta_time
from adastra_library.adastra_library.task import Task
from adastra_library.adastra_library.unique_object import UniqueObject

DELTAS = {
    delta_time.DAILY: {'days': +1},
    delta_time.WEEKLY: {'weeks': +1},
    delta_time.MONTHLY: {'months': +1},
    delta_time.YEARLY: {'years': +1}
}


class PlanManager(UniqueObject):
    """

    PlanManager is used to plan tasks in determined task list
    with some time delta. Also can have start and end dates of
    plan. Needs a TaskPattern instance.
    """
    def __init__(self,
                 delta,
                 task_pattern,
                 task_list_id,
                 start_date=None,
                 end_date=None,
                 last_created=None,
                 unique_id=None):
        super(PlanManager, self).__init__(name="Plan Manager", unique_id=unique_id)
        self.delta = delta
        self.task_list_id = task_list_id
        self.start_date = start_date
        self.end_date = end_date
        self.task_pattern = task_pattern
        self.last_created = last_created if last_created is not None else\
            start_date - relativedelta(**DELTAS.get(delta)) if start_date else datetime.now()

    def get_planned_tasks(self, current_date):
        """
        :param current_date: a date until which
        user wants to get tasks
        :return: returns planned tasks which weren't returned
        earlier and a task list id to which tasks should be appended
        """
        tasks = []
        if self.start_date is not None and current_date < self.start_date:
            return tasks

        print(self.delta)
        delta = relativedelta(**DELTAS.get(self.delta))
        while self.last_created < current_date - delta and \
                (self.end_date is None or
                 self.last_created < self.end_date - delta):
            tasks.append(Task(**self.task_pattern.get_task_create_params()))
            self.last_created += delta

        return tasks, self.task_list_id
