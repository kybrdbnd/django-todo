from rest_framework.serializers import ModelSerializer
from todo.models import (Company, Project, Task)

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
            'task',
            'members'
        ]


class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'task',
            'members'
        ]


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'task',
            'members'
        ]

# task


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


class TaskListSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'created_by',
            'assigned_to'
        ]
