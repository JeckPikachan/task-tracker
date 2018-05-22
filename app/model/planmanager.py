import time

from app.model.task import Task


class PlanManager:
    def __init__(self,
                 delta,
                 task_pattern,
                 task_list_id,
                 start_date=None,
                 end_date=None,
                 last_created=None):
        self.delta = delta
        self.task_list_id = task_list_id
        self.start_date = start_date
        self.end_date = end_date
        self.task_pattern = task_pattern
        self.last_created = last_created if last_created is not None else\
            start_date - delta if start_date else time.time()

    def get_planned_tasks(self, current_time):
        tasks = []
        if self.start_date is not None and current_time < self.start_date:
            return tasks

        while self.last_created < current_time - self.delta and \
                (self.end_date is None or
                 self.last_created < self.end_date - self.delta):
            tasks.append(Task(**self.task_pattern.get_task_create_params()))
            self.last_created += self.delta

        return tasks, self.task_list_id
