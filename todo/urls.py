from django.conf.urls import url
from .views import (project, send_invite, add_project, add_task, add_member)

urlpatterns = [
    url(r'^$', project, name='project'),
    url(r'^add_project/', add_project, name='add_project'),
    url(r'^send_invite/', send_invite, name='send_invite'),
    url(r'^add_task/', add_task, name='add_task'),
    url(r'^add_member/', add_member, name='add_member')
]
