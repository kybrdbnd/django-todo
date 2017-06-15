from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, related_name='created_by')
    assigned_to = models.ForeignKey(User, null=True,
                                    blank=True,
                                    related_name='assigned_to')

    def __str__(self):
        return self.name


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    name = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, blank=True)
    members = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    name = models.CharField(max_length=100)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project, blank=True)

    def __str__(self):
        return self.name
