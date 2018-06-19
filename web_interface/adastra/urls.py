from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = "adastra"


users_patterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'adastra:home'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
]

projects_patterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'^create/$', views.create_project, name='create_project'),
    url(r'^edit/(?P<project_id>[0-9]+)/$', views.edit_project, name='edit_project'),
    url(r'^delete/(?P<project_id>[0-9]+)/$', views.delete_project, name='delete_project')
]

tasks_patterns = [
    url(r'^(?P<project_id>[0-9]+)/$', views.tasks, name='tasks'),
    url(r'^create/(?P<project_id>[0-9]+)/(?P<task_list_id>[0-9]+)/$', views.create_task, name='create_task'),
]

task_lists_patterns = [
    url(r'^create/(?P<project_id>[0-9]+)/$', views.create_task_list, name='create_task_list'),
    url(r'^delete/(?P<project_id>[0-9]+)/(?P<task_list_id>[0-9]+)/$', views.delete_task_list, name='delete_task_list'),
    url(r'^edit/(?P<project_id>[0-9]+)/(?P<task_list_id>[0-9]+)/$', views.edit_task_list, name='edit_task_list')
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^users/', include(users_patterns)),
    url(r'^projects/', include(projects_patterns)),
    url(r'^tasks/', include(tasks_patterns)),
    url(r'^task_lists/', include(task_lists_patterns))
]
