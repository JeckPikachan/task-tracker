from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput, ModelChoiceField, DateInput

from .models import ProjectModel, TaskListModel, TaskModel


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


class TaskForm(ModelForm):
    task_list = ModelChoiceField(
        queryset=TaskListModel.objects.all(),
        widget=HiddenInput()
    )
    author = ModelChoiceField(
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = TaskModel
        fields = ['name', 'description', 'expiration_date',
                  'status', 'priority', 'author', 'task_list']
        widgets = {
            'expiration_date': DateInput(attrs={'class': 'datepicker'}),
        }