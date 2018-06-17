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
    url(r'^create/$', views.create_project, name='create_project')
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^users/', include(users_patterns)),
    url(r'^projects/', include(projects_patterns))
]
