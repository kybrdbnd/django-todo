from django.contrib import admin
from .models import (Profile, Project, Task, Company)
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'first_name', 'last_name',)

    def get_user(self, obj):
        return obj.user.username


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Company, CompanyAdmin)
