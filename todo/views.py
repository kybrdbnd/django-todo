from django.shortcuts import render, get_object_or_404, redirect
from .forms import (ProfileForm, ProjectForm, RoleForm)
from .models import (Project, Profile, Employee, Company, Task)
from datetime import datetime, timedelta
from django.http import JsonResponse
from invitations.models import Invitation
from random import choice
from string import ascii_lowercase, digits
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    if request.user.is_authenticated():
        return redirect('todo:project')
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'home.html', context)


def project(request):
    d1 = datetime.now()
    date_range = []
    for i in range(7):
        date_range.append(d1 + timedelta(days=i))
    for i in range(7):
        date_range.append(d1 - timedelta(days=i))
    date_range = sorted(set(date_range))

    context = {
        'date_range': date_range
    }
    current_user_email = request.user.email
    i = Invitation.objects.filter(email=current_user_email)
    if not i.exists():
        return render(request, 'project.html', context)
    else:
        if i[0].accepted:
            return render(request, 'project.html', context)
        else:
            return render(request, 'error_invitation.html', {})


def profile(request):
    instance = get_object_or_404(User, id=request.user.id)
    employee = get_object_or_404(Employee, user=instance)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=instance)
        role_form = RoleForm(request.POST, instance=employee)
        if form.is_valid() and role_form.is_valid():
            form.save()
            role_form.save()
    else:
        form = ProfileForm(instance=instance)
        role_form = RoleForm(instance=employee)
    context = {
        'form': form,
        'role_form': role_form
    }
    return render(request, 'profile.html', context)


def manage_profile(request):
    project_form = ProjectForm()
    employee = get_object_or_404(Employee, user=request.user)
    company = employee.company_set.all()[0]
    if company.owner == request.user:
        owner = True
    else:
        owner = False
    if employee.role.name == 'Project Manager':
        project_manager = True
    else:
        project_manager = False
    context = {
        'owner': owner,
        'project_manager': project_manager,
        'project_form': project_form
    }
    return render(request, 'manage.html', context)


def add_project(request):
    employee = get_object_or_404(Employee, user=request.user)
    company = employee.company_set.all()[0]
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
