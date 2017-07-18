from django import template
from ..models import Role
register = template.Library()


@register.filter
def managers(project_members):
    role = Role.objects.get(name='Project Manager')
    return project_members.filter(role=role)


@register.filter
def tasks(project_tasks, project_name):
    return project_tasks.filter(percentage_complete__lte=100).filter(project__name=project_name)[:5][::-1]
