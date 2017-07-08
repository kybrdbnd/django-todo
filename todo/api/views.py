from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView)
from rest_framework.mixins import (RetrieveModelMixin, ListModelMixin)

from django.shortcuts import get_object_or_404
from .serializers import (CompanyListSerializer,
                          ProjectListSerializer, ProjectDetailSerializer,
                          InivitationSerializer, TaskListSerializer)
from todo.models import (Project, Employee)
from invitations.models import Invitation


# company

class CompanyListView(ListAPIView):
    serializer_class = CompanyListSerializer

    def get_queryset(self, *args, **kwargs):
        employee = Employee.objects.get(user=self.request.user)
        company = employee.company_set.all()
        return company


# project

class ProjectDetailView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class ProjectTaskListView(ListModelMixin, RetrieveAPIView):
    serializer_class = TaskListSerializer

    def get_queryset(self, *args, **kwargs):
        project = kwargs.get('project')
        employee = get_object_or_404(Employee, user=self.request.user)
        project_tasks = project.tasks.all().filter(assigned_to=employee)
        return project_tasks

    def get_object(self, *args, **kwargs):
        project_id = self.kwargs.get('pk')
        project = Project.objects.get(id=project_id)
        queryset = self.get_queryset(project=project)
        # return queryset


class ProjectListView(ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self, *args, **kwargs):
        employee = Employee.objects.get(user=self.request.user)
        projects = employee.project_set.all()
        return projects


class InvitationListView(ListAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InivitationSerializer
