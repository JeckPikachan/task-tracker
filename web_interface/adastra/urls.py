from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = "adastra"

users_patterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'adastra:home'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
]

exact_task_patterns = [
    url(r'^delete/$', views.delete_task, name='delete_task'),
    url(r'^$', views.show_task, name='show_task'),
    url(r'^edit/$', views.edit_task, name='edit_task')
]

exact_task_list_patterns = [
    url(r'^delete/$', views.delete_task_list, name='delete_task_list'),
    url(r'^edit/$', views.edit_task_list, name='edit_task_list'),
    url(r'^create_task/$', views.create_task, name='create_task'),
]

task_lists_patterns = [
    url(r'^create/$', views.create_task_list, name='create_task_list'),
    url(r'^(?P<task_list_id>[0-9]+)/', include(exact_task_list_patterns)),
]

exact_plan_patterns = [
    url(r'^edit/$', views.edit_plan, name='edit_plan')
]

plans_patterns = [
    url(r'^$', views.plans, name='plans'),
    url(r'^create/$', views.create_plan, name='create_plan'),
    url(r'^(?P<plan_id>[0-9]+)/', include(exact_plan_patterns))
]

exact_project_patterns = [
    url(r'^$', views.tasks, name='tasks'),
    url(r'^edit/$', views.edit_project, name='edit_project'),
    url(r'^delete/$', views.delete_project, name='delete_project'),
    url(r'^task_list/', include(task_lists_patterns)),
    url(r'^task/(?P<task_id>[0-9]+)/', include(exact_task_patterns)),
    url(r'^plan/', include(plans_patterns))
]

projects_patterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'^(?P<project_id>[0-9]+)/', include(exact_project_patterns)),
    url(r'^create/$', views.create_project, name='create_project'),
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^users/', include(users_patterns)),
    url(r'^project/', include(projects_patterns)),
]
