from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import UserProjectRelationModel, ProjectModel
from . import storage
from .forms import ProjectForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('adastra:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def home(request):
    username = 'guest'
    if request.user.is_authenticated():
        username = request.user.username
    return render(
        request, 'adastra/home.html',
        {'username': username, 'nav_bar': 'home'})


@login_required
def projects(request):
    user_projects = storage.get_user_projects(request.user)
    return render(
        request, 'adastra/projects.html',
        {'user_projects': user_projects, 'nav_bar': 'projects'})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = ProjectModel(name=form.cleaned_data['name'])
            storage.save_project(project)
            upr = UserProjectRelationModel(user=request.user, project=project)
            storage.save_user_project_relation(upr)
            return redirect('adastra:projects')
    else:
        form = ProjectForm()

    return render(
        request, 'adastra/create_project.html',
        {'form': form, 'nav_bar': 'projects'}
    )


@login_required
def edit_project(request, project_id):
    project = storage.get_project_by_id(project_id)
    if project is None:
        return redirect('adastra:projects')
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project.name = form.cleaned_data['name']
            storage.save_project(project)
            return redirect('adastra:projects')
    else:
        form = ProjectForm(initial={'name': project.name})
    return render(
        request, 'adastra/edit_project.html',
        {'form': form, 'nav_bar': 'projects'}
    )


@login_required
def delete_project(request, project_id):
    if request.method == 'POST':
        storage.remove_project_by_id(project_id)
    return redirect('adastra:projects')


def tasks(request, project_id):
    project = storage.get_project_by_id(project_id)
    task_lists = storage.get_task_lists_by_project(project)
    return render(
        request, 'adastra/tasks.html',
        {
            'project': project,
            'task_lists': task_lists,
            'nav-bar': 'projects'
        }
    )
