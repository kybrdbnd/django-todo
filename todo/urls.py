from django.conf.urls import url
from .views import (project, send_invite, add_project,
                    add_task, add_member, assign_yourself, assign_other,
                    task_percentage)

urlpatterns = [
    url(r'^$', project, name='project'),
    url(r'^add_project/', add_project, name='add_project'),
    url(r'^send_invite/', send_invite, name='send_invite'),
    url(r'^add_task/', add_task, name='add_task'),
    url(r'^add_member/', add_member, name='add_member'),
    url(r'^assign_yourself/', assign_yourself, name='assign_yourself'),
    url(r'^assign_other/', assign_other, name='assign_other'),
    url(r'^task_percentage/', task_percentage, name='task_percentage')
]
