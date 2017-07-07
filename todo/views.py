from django.shortcuts import render, get_object_or_404
from .forms import (ProfileForm, ProjectForm)
from .models import (Project, Profile, Employee, Company, Task)
# from datetime import datetime, timedelta
from django.http import JsonResponse
from invitations.models import Invitation
from random import choice
from string import ascii_lowercase, digits
from django.contrib.auth.models import User
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
    current_user_email = request.user.email
    i = Invitation.objects.filter(email=current_user_email)
    if not i.exists():
        return render(request, 'project.html', {})
    else:
        if i[0].accepted:
            return render(request, 'project.html', {})
        else:
            return render(request, 'error_invitation.html', {})


def profile(request):
    instance = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=instance)
    context = {
        'form': form
    }
    return render(request, 'profile.html', context)


def manage_profile(request):
    project_form = ProjectForm()
    context = {
        'project_form': project_form
    }
    return render(request, 'manage.html', context)


def add_project(request):
    company = get_object_or_404(Company, owner=request.user)
    project = Project()
    project_name = request.POST.get('project_name')
    project.name = project_name
    project.save()
    company.projects.add(project)
    employee = get_object_or_404(Employee, user=request.user)
    project.members.add(employee)
    data = {
        'status': True
    }
    return JsonResponse(data)


def generate_random_username(length=8,
                             chars=ascii_lowercase + digits,
                             split=4,
                             delimiter='-'):

    username = ''.join([choice(chars) for i in range(length)])

    if split:
        username = delimiter.join([username[start:start + split]
                                   for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(length=length,
                                        chars=chars,
                                        split=split,
                                        delimiter=delimiter)
    except User.DoesNotExist:
        return username


def send_invite(request):
    inviter_email = request.POST.get('email')
    invite = Invitation.create(inviter_email, inviter=request.user)
    user = User.objects.create_user(generate_random_username(),
                                    inviter_email,
                                    'demo1234')
    user.save()
    profile = Profile.objects.create(user=user)
    profile.save()
    employee = Employee.objects.create(user=user)
    employee.save()
    company = get_object_or_404(Company, owner=request.user)
    company.employees.add(employee)
    invite.send_invitation(request)
    data = {
        'status': True
    }
    return JsonResponse(data)


def accept_invitation(request):
    return render(request, 'accept_invitation.html', {})


def add_task(request):
    project_id = request.POST.get('project_id')
    task_name = request.POST.get('task_name')
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=request.user.id)
    employee_instance = get_object_or_404(Employee, user=user)
    task_instance = Task.objects.create(name=task_name,
                                        created_by=employee_instance)
    task_instance.save()
    project.tasks.add(task_instance)
    data = {
        'status': True
    }
    return JsonResponse(data)


def add_member(request):
    project_id = request.POST.get('project_id')
    member_id = request.POST.get('member_id')
    project = get_object_or_404(Project, id=project_id)
    member = get_object_or_404(User, id=member_id)
    if project.members.filter(user=member).exists():
        return JsonResponse({'status': False,
                             'message': 'Member already exists'})
    else:
        employee = get_object_or_404(Employee, user=member)
        project.members.add(employee)
        return JsonResponse({'status': True,
                             'message': 'Member Successfully added'})
