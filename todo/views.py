from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from .forms import (ProjectForm)
from .models import (Project, Company, Task)
from datetime import datetime, timedelta
# Create your views here.


def home(request):
    projects = Project.objects.all()
    # data = {}
    # if request.method == 'POST':
    #     form = ProjectForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         data = {
    #             'success': 'Successfully Added'
    #         }
    # return HttpResponse(json.dumps(data), content_type='application/json')

    # else:
    #     form = ProjectForm()
    context = {
        'projects': projects
    }
    return render(request, 'home.html', context)


def project(request):
    projects = request.user.project_set.all()
    d1 = datetime.now()
    date_range = []
    for i in range(7):
        date_range.append(d1 + timedelta(days=i))
    for i in range(7):
        date_range.append(d1 - timedelta(days=i))
    # print(set(date_range))
    date_range = sorted(set(date_range))
    context = {
        'projects': projects,
        'date_range': date_range
    }
    return render(request, 'project.html', context)
