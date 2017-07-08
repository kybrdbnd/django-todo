from django.conf.urls import url
from .views import (ProjectListView, ProjectDetailView,
                    CompanyListView, ProjectTaskListView,
                    InvitationListView)

urlpatterns = [

    url(r'^$', ProjectListView.as_view(), name='project_list'),
    url(r'^project/(?P<pk>\d+)/task/',
        ProjectTaskListView.as_view(), name='project_task_detail'),
    url(r'^project/(?P<pk>\d+)/$',
        ProjectDetailView.as_view(), name='project_detail'),
    url(r'^company/', CompanyListView.as_view(), name='company'),
    url(r'^invitations/', InvitationListView.as_view(), name='invitations'),
]
