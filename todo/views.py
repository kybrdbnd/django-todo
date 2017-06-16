from django.shortcuts import render, redirect, get_object_or_404
from .forms import (ProjectForm, ProfileForm)
from .models import (Project, Company, Task, Profile, Employee)
from datetime import datetime, timedelta
# Create your views here.


def home(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'home.html', context)


def project(request):
    # projects = request.user.project_set.all()
    # d1 = datetime.now()
    # date_range = []
    # for i in range(7):
    #     date_range.append(d1 + timedelta(days=i))
    # for i in range(7):
    #     date_range.append(d1 - timedelta(days=i))
    # # print(set(date_range))
    # date_range = sorted(set(date_range))

    # context = {
    #     'projects': projects,
    #     'date_range': date_range
    # }
    return render(request, 'project.html', {})


def profile(request):
    if request.method == 'POST':
        try:
            instance = Profile.objects.get(user=request.user)
            form = ProfileForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('todo:project')
        except Profile.DoesNotExist:
            form = ProfileForm(request.POST)
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.user = request.user
                form_instance.save()
                return redirect('todo:project')
    else:
        try:
            instance = Profile.objects.get(user=request.user)
            form = ProfileForm(instance=instance)
        except Profile.DoesNotExist:
            form = ProfileForm()
        context = {
            'form': form
        }
    return render(request, 'profile.html', context)


def manage_profile(request):
    employee = Employee.objects.get(profile=request.user.profile)
    company = employee.company_set.all()[0]
    projects = employee.project_set.all()
    context = {
        'company': company,
        'projects': projects
    }
    return render(request, 'manage.html', context)
