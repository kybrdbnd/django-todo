from rest_framework.serializers import ModelSerializer
from todo.models import (Company, Project, Task, Employee, Profile)
from django.contrib.auth.models import User
from invitations.models import Invitation


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username'

        ]


class ProfileListSerializer(ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'user', 'full_name']


class EmployeePageSerializer(ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'role', 'project_set',
                  'company_set', 'assigned_to']
        depth = 1


class EmployeeListSerializer(ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'role']
        depth = 1


class TaskListSerializer(ModelSerializer):
    created_by = EmployeeListSerializer()
    assigned_to = EmployeeListSerializer()

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'created_at',
            'created_by',
            'assigned_to',
            'assigned_date',
            'percentage_complete'
        ]


class ProjectListSerializer(ModelSerializer):
    tasks = TaskListSerializer(many=True)
    members = EmployeeListSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'tasks',
            'members'
        ]


class CompanyListSerializer(ModelSerializer):
    owner = UserListSerializer()
    projects = ProjectListSerializer(many=True)
    employees = EmployeeListSerializer(many=True)

    class Meta:
        model = Company
        fields = [
            'name',
            'owner',
            'projects',
            'employees'
        ]


class ProjectDetailSerializer(ModelSerializer):
    tasks = TaskListSerializer(many=True)
    members = EmployeeListSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'tasks',
            'members'
        ]


class InivitationSerializer(ModelSerializer):
    inviter = UserListSerializer()

    class Meta:
        model = Invitation
        fields = ['email',
                  'inviter']
