from django.contrib import admin
from .models import (Profile, Project, Task, Company, Employee)
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user']

    def get_user(self, obj):
        return obj.user.username


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_owner', 'created_at', 'get_employees')

    def get_owner(self, obj):
        return obj.owner.username

    def get_employees(self, obj):
        return ', '.join([employee.user.username for employee in obj.employees.all()])


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'joined_at')

    def get_user(self, obj):
        return obj.user.username


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
