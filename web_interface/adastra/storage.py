from adastra_library import Project
from django.core.exceptions import ObjectDoesNotExist

from .models import UserProjectRelationModel, ProjectModel, TaskListModel, TaskModel, TaskRelationModel, PlanModel


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
    except ObjectDoesNotExist:
        return None


def remove_project_by_id(project_id):
    project = get_project_by_id(project_id)
    if project is not None:
        project.delete()


def get_task_lists_by_project(project):
    return project.tasklistmodel_set.all()


def get_task_list_by_id(task_list_id):
    try:
        return TaskListModel.objects.get(id=task_list_id)
    except ObjectDoesNotExist:
        return None


def save_task_list(task_list):
    task_list.save()


def remove_task_list_by_id(task_list_id):
    task_list = get_task_list_by_id(task_list_id)
    if task_list_id is not None:
        task_list.delete()


def save_task(task):
    task.save()


def get_task_by_id(task_id):
    try:
        return TaskModel.objects.get(id=task_id)
    except ObjectDoesNotExist:
        return None


def remove_task_by_id(task_id):
    task = get_task_by_id(task_id)
    if task is not None:
        task.delete()


def get_tasks_by_project(project):
    task_lists = project.tasklistmodel_set.all()
    tasks = []
    for task_list in task_lists:
        tasks.extend(task_list.taskmodel_set.all())

    return tasks


def get_task_relation_by_two_tasks(task_to, task_from):
    try:
        return TaskRelationModel.objects.get(task_to=task_to, task_from=task_from)
    except ObjectDoesNotExist:
        return None


def get_task_relations_by_task_from(task_from):
    return list(TaskRelationModel.objects.filter(task_from=task_from))


def save_task_relation(task_relation):
    task_relation.save()


def update_task_relations(task_from, task_to_ids):
    tasks_to = [get_task_by_id(task_to_id) for task_to_id in task_to_ids]
    for task_to in tasks_to:
        task_relation = get_task_relation_by_two_tasks(task_to, task_from)
        if task_relation is None:
            task_relation = TaskRelationModel(task_from=task_from, task_to=task_to, description='')
            save_task_relation(task_relation)

    task_relations_to_be_deleted = TaskRelationModel.objects.filter(task_from=task_from)
    for task_to in tasks_to:
        task_relations_to_be_deleted = task_relations_to_be_deleted.exclude(
            task_to=task_to
        )

    task_relations_to_be_deleted.delete()


def save_task_pattern(task_pattern):
    task_pattern.save()


def save_plan(plan):
    plan.save()


def get_plan_by_id(plan_id):
    try:
        return PlanModel.objects.get(id=plan_id)
    except ObjectDoesNotExist:
        return None


def get_plans_by_task_list(task_list):
    return task_list.planmodel_set.all()


def get_plans_by_project(project):
    task_lists = get_task_lists_by_project(project)
    plans_list = []

    for task_list in task_lists:
        plans_list.extend(get_plans_by_task_list(task_list))

    return plans_list
