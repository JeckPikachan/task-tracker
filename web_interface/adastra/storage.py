from adastra_library import Project

from .models import UserProjectRelationModel, ProjectModel


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
