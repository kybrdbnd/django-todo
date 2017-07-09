from django.conf.urls import url
from .views import (ProjectListView, ProjectDetailView,
                    CompanyListView, ProjectTaskListView,
                    InvitationListView, EmployeePageView)

urlpatterns = [

    url(r'^$', ProjectListView.as_view(), name='project_list'),
    url(r'^project/(?P<pk>\d+)/task/date/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$',
        ProjectTaskListView.as_view(), name='project_task_detail'),
    url(r'^project/(?P<pk>\d+)/$',
        ProjectDetailView.as_view(), name='project_detail'),
    url(r'^company/', CompanyListView.as_view(), name='company'),
    url(r'^employee/(?P<pk>\d+)/$',
        EmployeePageView.as_view(), name='employee_page'),
    url(r'^invitations/', InvitationListView.as_view(), name='invitations'),
]
