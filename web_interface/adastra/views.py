from datetime import date

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import render, redirect

from . import storage
from .forms import ProjectForm, TaskListForm, TaskForm, PlanForm, UserAddForm
from .models import UserProjectRelationModel, ProjectModel, TaskListModel, TaskModel, TaskPatternModel, PlanModel


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


@login_required
def tasks(request, project_id):
    project = storage.get_project_by_id(project_id)
    task_lists = storage.get_task_lists_by_project(project)

    plans_list = storage.get_plans_by_project(project)
    for plan in plans_list:
        for task in plan.get_planned_tasks(date.today()):
            storage.save_task(task)
        storage.save_plan(plan)

    return render(
        request, 'adastra/tasks.html',
        {
            'project': project,
            'task_lists': task_lists,
        }
    )


@login_required
def create_task_list(request, project_id):
    project = storage.get_project_by_id(project_id)
    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            task_list = TaskListModel(
                name=form.cleaned_data['name'],
                project=form.cleaned_data['project']
            )
            storage.save_task_list(task_list)
            return redirect('adastra:tasks', project_id)
    else:
        form = TaskListForm(initial={'project': project})

    return render(
        request, 'adastra/create_task_list.html',
        {'form': form, 'project': project}
    )


@login_required
def delete_task_list(request, project_id, task_list_id):
    if request.method == 'POST':
        storage.remove_task_list_by_id(task_list_id)
    return redirect('adastra:tasks', project_id)


@login_required
def edit_task_list(request, project_id, task_list_id):
    task_list = storage.get_task_list_by_id(task_list_id)
    if task_list is None:
        return redirect('adastra:tasks', project_id)
    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            task_list.name = form.cleaned_data['name']
            storage.save_task_list(task_list)
            return redirect('adastra:tasks', project_id)
    else:
        form = TaskListForm(initial={'name': task_list.name, 'project': task_list.project})
    return render(
        request, 'adastra/edit_task_list.html',
        {'form': form, 'nav_bar': 'projects'}
    )


@login_required
def create_task(request, project_id, task_list_id):
    task_list = storage.get_task_list_by_id(task_list_id)
    project = storage.get_project_by_id(project_id)
    if request.method == 'POST':
        form = TaskForm(project, request.POST)
        if form.is_valid():
            task = TaskModel(
                name=form.cleaned_data['name'],
                task_list=form.cleaned_data['task_list'],
                author=form.cleaned_data['author'],
                description=form.cleaned_data['description'],
                expiration_date=form.cleaned_data['expiration_date'],
                status=form.cleaned_data['status'],
                priority=form.cleaned_data['priority']
            )
            storage.save_task(task)

            storage.update_task_relations(task, form.cleaned_data['related_tasks'])

            return redirect('adastra:tasks', project_id)
    else:
        form = TaskForm(project, initial={'task_list': task_list, 'author': request.user})

    return render(
        request, 'adastra/create_task.html',
        {'form': form}
    )


@login_required
def delete_task(request, project_id, task_id):
    if request.method == 'POST':
        storage.remove_task_by_id(task_id)
    return redirect('adastra:tasks', project_id)


@login_required
def show_task(request, project_id, task_id):
    task = storage.get_task_by_id(task_id)
    project = storage.get_project_by_id(project_id)
    if task is None or project is None:
        return Http404()
    else:
        task_relations = storage.get_task_relations_by_task_from(task)
        related_tasks = [task_relation.task_to for task_relation in task_relations]
        return render(
            request, 'adastra/show_task.html',
            {'task': task, 'project': project, 'related_tasks': related_tasks}
        )


@login_required
def edit_task(request, project_id, task_id):
    task = storage.get_task_by_id(task_id)
    project = storage.get_project_by_id(project_id)
    if task is None:
        return redirect('adastra:tasks', project_id)
    if request.method == 'POST':
        form = TaskForm(project, request.POST)
        if form.is_valid():
            task.author = form.cleaned_data['author']
            task.task_list = form.cleaned_data['task_list']
            task.name = form.cleaned_data['name']
            task.description = form.cleaned_data['description']
            task.expiration_date = form.cleaned_data['expiration_date']
            task.status = form.cleaned_data['status']
            task.priority = form.cleaned_data['priority']

            storage.save_task(task)

            storage.update_task_relations(task, form.cleaned_data['related_tasks'])

            return redirect('adastra:tasks', project_id)
    else:
        task_relations = storage.get_task_relations_by_task_from(task)
        chosen_tasks_ids = [task_relation.task_to.id for task_relation in task_relations]
        form = TaskForm(project, initial={
            'task_list': task.task_list,
            'author': task.author,
            'name': task.name,
            'description': task.description,
            'expiration_date': task.expiration_date,
            'status': task.status,
            'priority': task.priority,
            'related_tasks': chosen_tasks_ids
        })

    return render(
        request, 'adastra/edit_task.html',
        {'form': form}
    )


@login_required
def plans(request, project_id):
    project = storage.get_project_by_id(project_id)
    if project is None:
        return Http404()
    plans_list = storage.get_plans_by_project(project)

    return render(
        request, 'adastra/plans.html',
        {'project': project, 'plans': plans_list}
    )


@login_required
def create_plan(request, project_id):
    project = storage.get_project_by_id(project_id)
    if project is None:
        return Http404()
    if request.method == 'POST':
        form = PlanForm(project, request.POST)
        if form.is_valid():
            task_pattern = TaskPatternModel(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                status=form.cleaned_data['status'],
                priority=form.cleaned_data['priority'],
                author=form.cleaned_data['author']
            )
            storage.save_task_pattern(task_pattern)

            task_list = \
                storage.get_task_list_by_id(form.cleaned_data['task_list'])
            plan = PlanModel(
                delta=int(form.cleaned_data['delta']),
                task_pattern=task_pattern,
                task_list=task_list,
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date']
            )
            storage.save_plan(plan)

            return redirect('adastra:plans', project_id)
    else:
        form = PlanForm(project, initial={'author': request.user, 'start_date': date.today()})

    return render(
        request, 'adastra/create_plan.html',
        {'form': form}
    )


@login_required
def edit_plan(request, project_id, plan_id):
    project = storage.get_project_by_id(project_id)
    plan = storage.get_plan_by_id(plan_id)
    if project is None or plan is None:
        return Http404()
    if request.method == 'POST':
        form = PlanForm(project, request.POST)
        task_pattern = plan.task_pattern
        if form.is_valid():
            task_pattern.name = form.cleaned_data['name']
            task_pattern.description = form.cleaned_data['description']
            task_pattern.status = form.cleaned_data['status']
            task_pattern.priority = form.cleaned_data['priority']

            storage.save_task_pattern(task_pattern)

            task_list = \
                storage.get_task_list_by_id(form.cleaned_data['task_list'])
            plan.delta = int(form.cleaned_data['delta'])
            plan.task_list = task_list
            plan.start_date = form.cleaned_data['start_date']
            plan.end_date = form.cleaned_data['end_date']

            storage.save_plan(plan)

            return redirect('adastra:plans', project_id)
    else:
        form = PlanForm(
            project, initial={
                'name': plan.task_pattern.name,
                'description': plan.task_pattern.description,
                'status': plan.task_pattern.status,
                'priority': plan.task_pattern.priority,
                'author': plan.task_pattern.author,
                'delta': plan.delta,
                'task_list': plan.task_list.id,
                'start_date': plan.start_date,
                'end_date': plan.end_date
            }
        )

    return render(
        request, 'adastra/edit_plan.html',
        {'form': form}
    )


@login_required
def show_plan(request, project_id, plan_id):
    project = storage.get_project_by_id(project_id)
    plan = storage.get_plan_by_id(plan_id)
    if project is None or plan is None:
        return Http404()

    return render(
        request, 'adastra/show_plan.html',
        {'project': project, 'plan': plan}
    )


@login_required
def delete_plan(request, project_id, plan_id):
    if request.method == 'POST':
        storage.remove_plan_by_id(plan_id)
    return redirect('adastra:plans', project_id)


@login_required
def users(request, project_id):
    project = storage.get_project_by_id(project_id)
    if project is None:
        return Http404()
    users_list = storage.get_project_users(project)

    return render(
        request, 'adastra/users.html',
        {
            'users': users_list,
            'project': project,
            'current_user': request.user
        }
    )


@login_required
def add_user(request, project_id):
    project = storage.get_project_by_id(project_id)
    if project is None:
        return Http404()
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = storage.get_user_by_username(username)
            if user is None:
                form.add_error('username', 'No user with such username!')
            else:
                user_project_relation = \
                    storage.get_user_project_relation(user, project)

                if user_project_relation is None:
                    user_project_relation = \
                        UserProjectRelationModel(
                            project=project,
                            user=user
                        )
                    storage.save_user_project_relation(user_project_relation)

                return redirect('adastra:users', project_id)
    else:
        form = UserAddForm()

    return render(
        request, 'adastra/add_user.html',
        {'form': form}
    )


@login_required
def remove_user(request, project_id, user_id):
    if request.method == 'POST':
        user = storage.get_user_by_id(user_id)
        project = storage.get_project_by_id(project_id)
        storage.remove_user_project_relation(user, project)

        users_list = storage.get_project_users(project)
        if not users_list:
            storage.remove_project_by_id(project_id)
        if request.user == user:
            return redirect('adastra:projects')
    return redirect('adastra:users', project_id)
