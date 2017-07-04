from django.conf.urls import url
from .views import (project, send_invite, add_project, add_task)

urlpatterns = [
    url(r'^$', project, name='project'),
    url(r'^add_project/', add_project, name='add_project'),
    url(r'^send_invite/', send_invite, name='send_invite'),
    url(r'^add_task/', add_task, name='add_task'),
]
