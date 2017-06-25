from django.shortcuts import render, redirect, get_object_or_404
from .forms import (ProfileForm)
from .models import (Project, Profile, Employee, Company)
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
    return render(request, 'manage.html', {})


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
    employee = Employee.objects.create(profile=profile)
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
