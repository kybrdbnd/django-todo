from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     RetrieveUpdateAPIView)
from .serializers import (CompanyListSerializer, ProjectCreateSerializer,
                          ProjectListSerializer, ProjectDetailSerializer,
                          TaskCreateSerializer,
                          TaskListSerializer, TaskDetailSerializer)
from todo.models import (Company, Project, Task)


# company

class CompanyListView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer


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
        queryset = self.request.user.project_set.all()
        return queryset


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
