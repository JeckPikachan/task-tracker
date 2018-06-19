from django.contrib.auth.models import User
from django.db import models


class ProjectModel(models.Model):
    name = models.CharField(max_length=140)


class UserProjectRelationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)


class TaskListModel(models.Model):
    name = models.CharField(max_length=140)
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)


class TaskModel(models.Model):
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

    task_list = models.ForeignKey(TaskListModel, on_delete=models.CASCADE)

    name = models.CharField(max_length=140)
    description = models.CharField(blank=True, max_length=10000)
    expiration_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
