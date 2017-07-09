from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView)
from django.shortcuts import get_object_or_404
from .serializers import (CompanyListSerializer, EmployeePageSerializer,
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


class ProjectTaskListView(ListAPIView):
    serializer_class = TaskListSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get('pk')
        day = self.kwargs.get('day')
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        query_date = year + '-' + month + '-' + day
        project = Project.objects.get(id=project_id)
        employee = get_object_or_404(Employee, user=self.request.user)
        project_tasks = project.tasks.all().filter(
            assigned_to=employee).filter(assigned_date=query_date)
        return project_tasks


class ProjectListView(ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self, *args, **kwargs):
        employee = Employee.objects.get(user=self.request.user)
        projects = employee.project_set.all()
        return projects


class EmployeePageView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeePageSerializer


class InvitationListView(ListAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InivitationSerializer
