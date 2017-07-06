from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     RetrieveUpdateAPIView
                                     )
from .serializers import (CompanyListSerializer, ProjectCreateSerializer,
                          ProjectListSerializer, ProjectDetailSerializer,
                          TaskCreateSerializer,
                          TaskListSerializer, TaskDetailSerializer,
                          InivitationSerializer)
from todo.models import (Project, Task, Employee)
from invitations.models import Invitation


# company

class CompanyListView(ListAPIView):
    serializer_class = CompanyListSerializer

    def get_queryset(self, *args, **kwargs):
        employee = Employee.objects.get(user=self.request.user)
        company = employee.company_set.all()
        return company


# project

class ProjectCreateView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer


class ProjectDeleteView(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class ProjectDetailView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class ProjectListView(ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self, *args, **kwargs):
        employee = Employee.objects.get(user=self.request.user)
        projects = employee.project_set.all()
        return projects


class ProjectUpdateView(RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


# task
class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


class TaskDeleteView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class TaskDetailView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer


class TaskUpdateView(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class InvitationListView(ListAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InivitationSerializer
