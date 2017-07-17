from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(200, 300)],
                                      format='JPEG',
                                      options={'quality': 60})
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.user.username


class Role(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,
                                      auto_now=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    joined_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    user = models.OneToOneField(User, blank=True, null=True,
                                on_delete=models.CASCADE)
    role = models.ForeignKey(Role, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(Employee, related_name='created_by')
    assigned_to = models.ForeignKey(Employee,
                                    related_name='assigned_to',
                                    null=True, blank=True)

    assigned_date = models.DateField(blank=True, null=True)
    percentage_complete = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name


class Backlog(models.Model):
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    created_for = models.ForeignKey(Task)
    created_by = models.ForeignKey(Employee, null=True, blank=True)
    reason = models.CharField(max_length=100, null=True)


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    name = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, blank=True)
    members = models.ManyToManyField(Employee, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    name = models.CharField(max_length=100)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project, blank=True)
    employees = models.ManyToManyField(Employee, blank=True)

    def __str__(self):
        return self.name
