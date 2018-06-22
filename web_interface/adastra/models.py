from datetime import date

from adastra_library.adastra_library.plan_manager import DELTAS
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db import models

STATUS_CHOICES = (
    (0, "CREATED"),
    (1, "IN WORK"),
    (2, "DONE")
)
PRIORITY_CHOICES = (
    (0, "LOW"),
    (1, "MIDDLE"),
    (2, "HIGH")
)
DELTA_CHOICES = (
    (0, "DAILY"),
    (1, "WEEKLY"),
    (2, "MONTHLY"),
    (3, "YEARLY")
)


class ProjectModel(models.Model):
    name = models.CharField(max_length=140)


class UserProjectRelationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)


class TaskListModel(models.Model):
    name = models.CharField(max_length=140)
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)


class TaskModel(models.Model):
    STATUS_CHOICES = STATUS_CHOICES
    PRIORITY_CHOICES = PRIORITY_CHOICES

    task_list = models.ForeignKey(TaskListModel, on_delete=models.CASCADE)

    name = models.CharField(max_length=140)
    description = models.CharField(blank=True, max_length=10000)
    expiration_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)


class TaskRelationModel(models.Model):
    description = models.CharField(max_length=140, blank=True)
    task_from = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name='task_from')
    task_to = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name='task_to')


class TaskPatternModel(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=10000, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_task(self):
        return TaskModel(
            name=self.name,
            description=self.description,
            status=self.status,
            priority=self.priority,
            author=self.author
        )


class PlanModel(models.Model):
    delta = models.IntegerField(choices=DELTA_CHOICES)
    task_pattern = models.OneToOneField(TaskPatternModel, on_delete=models.CASCADE)
    task_list = models.ForeignKey(TaskListModel, on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True)
    last_created = models.DateField()

    def __init__(self, *args, **kwargs):
        super(PlanModel, self).__init__(*args, **kwargs)
        self.last_created = (self.last_created if
                             self.last_created is not None else
                             self.start_date - relativedelta(**DELTAS.get(self.delta)))

    def get_planned_tasks(self, current_date):
        tasks = []
        if self.start_date is not None and current_date < self.start_date:
            return tasks

        delta = relativedelta(**DELTAS.get(self.delta))
        while self.last_created <= current_date - delta and \
                (self.end_date is None or
                 self.last_created <= self.end_date - delta):
            planned_task = self.task_pattern.get_task()
            planned_task.task_list = self.task_list
            tasks.append(planned_task)
            self.last_created += delta

        return tasks
