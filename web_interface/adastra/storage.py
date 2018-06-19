from adastra_library import Project
from peewee import DoesNotExist

from .models import UserProjectRelationModel, ProjectModel, TaskListModel


def get_user_projects(user):
    project_models = \
        [upr.project for upr in UserProjectRelationModel.objects.filter(user=user)]

    return [
        Project(
            unique_id=project_model.id,
            name=project_model.name
        )
        for project_model in project_models
    ]


def save_project(project):
    project.save()


def save_user_project_relation(user_project_relation):
    user_project_relation.save()


def get_project_by_id(project_id):
    try:
        return ProjectModel.objects.get(id=project_id)
    except DoesNotExist:
        return None


def remove_project_by_id(project_id):
    project = get_project_by_id(project_id)
    if project is not None:
        project.delete()


def get_task_lists_by_project(project):
    return list(project.tasklistmodel_set.all())


def get_task_list_by_id(task_list_id):
    try:
        return TaskListModel.objects.get(id=task_list_id)
    except DoesNotExist:
        return None


def save_task_list(task_list):
    task_list.save()


def remove_task_list_by_id(task_list_id):
    task_list = get_task_list_by_id(task_list_id)
    if task_list_id is not None:
        task_list.delete()


def save_task(task):
    task.save()
