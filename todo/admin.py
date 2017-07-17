from django.contrib import admin
from .models import (Profile, Project, Task, Company, Employee, Role, Backlog)
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user']

    def get_user(self, obj):
        return obj.user.username


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by',
                    'assigned_to', 'assigned_date', 'get_project',
                    'percentage_complete')

    def get_project(self, obj):
        project = obj.project_set.all()[0]
        return project.name


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_owner', 'created_at', 'get_employees')

    def get_owner(self, obj):
        return obj.owner.username

    def get_employees(self, obj):
        return ', '.join([employee.user.username for employee in obj.employees.all()])


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'joined_at', 'role')

    def get_user(self, obj):
        return obj.user.username


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class BacklogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'get_task', 'task_creator', 'reason')

    def get_task(self, obj):
        return obj.created_for.name

    def task_creator(self, obj):
        return obj.created_by.user.username


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Backlog, BacklogAdmin)
