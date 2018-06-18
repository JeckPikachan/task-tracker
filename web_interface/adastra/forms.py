from django.forms import ModelForm, HiddenInput

from .models import ProjectModel, TaskListModel


class ProjectForm(ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['name']


class TaskListForm(ModelForm):
    class Meta:
        model = TaskListModel
        fields = ['name', 'id']
        widgets = {
            'id': HiddenInput()
        }
