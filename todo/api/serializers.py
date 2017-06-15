from rest_framework.serializers import ModelSerializer
from todo.models import (Company, Project, Task)
from django.contrib.auth.models import User


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'username'

        ]

# company


class CompanyListSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'name',
            'owner',
            'projects'
        ]

# project


class ProjectCreateSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'tasks',
            'members'
        ]


class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'tasks',
            'members'
        ]


class TaskListSerializer(ModelSerializer):
    created_by = UserListSerializer()
    assigned_to = UserListSerializer()

    class Meta:
        model = Task
        fields = [
            'id',
            'created_at',
            'name',
            'created_by',
            'assigned_to'
        ]


class ProjectListSerializer(ModelSerializer):
    tasks = TaskListSerializer(many=True)
    members = UserListSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'tasks',
            'members'
        ]


class TaskCreateSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'name',
            'created_by',
            'assigned_to'

        ]


class TaskDetailSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'created_by',
            'assigned_to'

        ]
