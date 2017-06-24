from django.conf.urls import url
from .views import (ProjectCreateView, ProjectListView, ProjectDetailView,
                    ProjectDeleteView, ProjectUpdateView,
                    TaskCreateView, TaskListView, TaskDetailView,
                    TaskDeleteView, TaskUpdateView, CompanyListView,
                    InvitationListView)

urlpatterns = [

    # Project
    url(r'^$', ProjectListView.as_view(), name='project_list'),
    url(r'^project/create/',
        ProjectCreateView.as_view(), name='project_create'),
    url(r'^project/(?P<pk>\d+)/$',
        ProjectDetailView.as_view(), name='project_detail'),
    url(r'^project/(?P<pk>\d+)/update$',
        ProjectUpdateView.as_view(), name='project_update'),
    url(r'^project/(?P<pk>\d+)/delete$',
        ProjectDeleteView.as_view(), name='project_delete'),

    # Task
    url(r'^task/create/',
        TaskCreateView.as_view(), name='task_create'),
    url(r'^task/(?P<pk>\d+)/$',
        TaskDetailView.as_view(), name='task_detail'),
    url(r'^task/(?P<pk>\d+)/update$',
        TaskUpdateView.as_view(), name='task_update'),
    url(r'^task/(?P<pk>\d+)/delete$',
        TaskDeleteView.as_view(), name='task_delete'),
    url(r'^task/', TaskListView.as_view(), name='task_list'),


    url(r'^company/', CompanyListView.as_view(), name='company'),
    url(r'^invitations/', InvitationListView.as_view(), name='invitations'),



]
