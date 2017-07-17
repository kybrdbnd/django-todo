from django.conf.urls import url
from .views import (project, send_invite, add_project,
                    add_task, add_member, assign_yourself, assign_other,
                    task_percentage, task_put_back, project_detail, milestone,
                    delete_task, delete_project)

urlpatterns = [
    url(r'^$', project, name='project'),
    url(r'^project_detail/(?P<id>\d+)', project_detail, name='project_detail'),
    url(r'^add_project/', add_project, name='add_project'),
    url(r'^milestone/', milestone, name='milestone'),
    url(r'^send_invite/', send_invite, name='send_invite'),
    url(r'^add_task/', add_task, name='add_task'),
    url(r'^add_member/', add_member, name='add_member'),
    url(r'^assign_yourself/', assign_yourself, name='assign_yourself'),
    url(r'^assign_other/', assign_other, name='assign_other'),
    url(r'^task_percentage/', task_percentage, name='task_percentage'),
    url(r'^task_put_back/', task_put_back, name='task_put_back'),
    url(r'^delete_task/(?P<id>\d+)/$', delete_task, name='delete_task'),
    url(r'^delete_project/(?P<id>\d+)/$', delete_project, name='delete_project'),
]
