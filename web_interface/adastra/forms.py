from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput, ModelChoiceField, DateInput, Form, CharField, Textarea, DateField, \
    ChoiceField, MultipleChoiceField

from . import storage
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


class TaskForm(Form):
    task_list = ModelChoiceField(
        queryset=TaskListModel.objects.all(),
        widget=HiddenInput()
    )
    author = ModelChoiceField(
        queryset=User.objects.all(),
        widget=HiddenInput()
    )
    name = CharField(max_length=140, required=True)
    description = CharField(
        max_length=10000,
        widget=Textarea,
        required=False
    )
    expiration_date = DateField(
        widget=DateInput(attrs={'class': 'datepicker'}),
        required=False
    )
    status = ChoiceField(
        choices=TaskModel.STATUS_CHOICES,
        required=True
    )
    priority = ChoiceField(
        choices=TaskModel.PRIORITY_CHOICES,
        required=True
    )

    def __init__(self, project, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['related_tasks'] = MultipleChoiceField(
            choices=self._get_related_tasks_options(project),
            required=False
        )

    def _get_related_tasks_options(self, project):
        tasks = storage.get_tasks_by_project(project)
        return [(task.id, task.name) for task in tasks]
