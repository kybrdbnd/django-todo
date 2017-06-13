from django.contrib import admin
from .models import (Project, Task, Company)
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Company, CompanyAdmin)
