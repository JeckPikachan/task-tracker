from django.forms import ModelForm

from .models import ProjectModel


class ProjectForm(ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['name']
