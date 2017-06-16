from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
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


class Employee(models.Model):
    joined_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    profile = models.OneToOneField(Profile, blank=True, null=True,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.full_name()


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(Employee, related_name='created_by')
    assigned_to = models.ForeignKey(Employee, null=True,
                                    blank=True,
                                    related_name='assigned_to')

    def __str__(self):
        return self.name


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
