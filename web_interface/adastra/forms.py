from django.forms import ModelForm, HiddenInput, ModelChoiceField

from .models import ProjectModel, TaskListModel


class ProjectForm(ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['name']


class TaskListForm(ModelForm):
    project = ModelChoiceField(
        queryset=ProjectModel.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = TaskListModel
        fields = ['name', 'project']
