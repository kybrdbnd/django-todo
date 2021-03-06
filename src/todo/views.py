from django.shortcuts import render, get_object_or_404, redirect
from .forms import (ProfileForm, ProjectForm, MileStoneForm)
from .models import (Project, Profile, Employee, Task, Role, Backlog)
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from xlsxwriter.workbook import Workbook
from invitations.models import Invitation
from random import choice
from string import ascii_lowercase, digits
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    if request.user.is_authenticated():
        return redirect('todo:project')
    return render(request, 'colaborar/home.html', {})


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
        return render(request, 'colaborar/project.html', context)
    else:
        if i[0].accepted:
            return render(request, 'colaborar/project.html', context)
        else:
            return render(request, 'invitation/error_invitation.html', {})


def profile(request):
    instance = get_object_or_404(User, id=request.user.id)
    employee = get_object_or_404(Employee, user=instance)
    role = employee.role
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=instance)
    context = {
        'form': form,
        'role': role
    }
    return render(request, 'colaborar/profile.html', context)


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
    return render(request, 'colaborar/manage.html', context)


def add_project(request):
    employee = get_object_or_404(Employee, user=request.user)
    company = employee.company_set.all()[0]
    project = Project()
    project_name = request.POST.get('project_name')
    project.name = project_name
    project.created_by = employee
    project.save()
    company.projects.add(project)
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
    role = get_object_or_404(Role, name="Tester")
    employee = Employee.objects.create(user=user, role=role)
    employee.save()
    employee_instance = get_object_or_404(Employee, user=request.user)
    company = employee_instance.company_set.all()[0]
    company.employees.add(employee)
    invite.send_invitation(request)
    data = {
        'status': True
    }
    return JsonResponse(data)


def accept_invitation(request):
    return render(request, 'invitation/accept_invitation.html', {})


def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    total_tasks_count = project.tasks.count()
    ongoing_tasks_count = project.tasks.filter(percentage_complete__gte=0,
                                               percentage_complete__lt=100).count()
    completed_tasks_count = project.tasks.filter(
        percentage_complete=100).count()
    stats_data = [
        ['Total Tasks', total_tasks_count],
        ['Completed Tasks', completed_tasks_count],
        ['Ongoing Tasks', ongoing_tasks_count]
    ]
    context = {
        'project': project,
        'stats_data': stats_data,
        'max_limit': total_tasks_count + 50
    }
    return render(request, 'colaborar/project_detail.html', context)


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


def assign_yourself(request):
    task_id = request.POST.get('task_id')
    task_assigned_date = request.POST.get('task_date')
    format_date = datetime.strptime(task_assigned_date, '%d %B, %Y')
    new_date = datetime.strftime(format_date, '%Y-%m-%d')
    task = get_object_or_404(Task, id=task_id)
    employee = get_object_or_404(Employee, user=request.user)
    task.assigned_to = employee
    task.assigned_date = new_date
    task.save()
    return JsonResponse({'status': True,
                         'message': 'Task Successfully Assigned to You'})


def assign_other(request):
    task_id = request.POST.get('task_id')
    task_assigned_date = request.POST.get('task_date')
    employee_username = request.POST.get('task_member')
    user_instance = get_object_or_404(User, username=employee_username)
    employee = get_object_or_404(Employee, user=user_instance)
    format_date = datetime.strptime(task_assigned_date, '%d %B, %Y')
    new_date = datetime.strftime(format_date, '%Y-%m-%d')
    task = get_object_or_404(Task, id=task_id)
    task.assigned_to = employee
    task.assigned_date = new_date
    task.save()
    return JsonResponse({'status': True,
                         'message': 'Task Successfully Assigned To ' + employee_username})


def task_percentage(request):
    task_id = request.POST.get('task_id')
    task_percentage = request.POST.get('task_percentage')
    task = get_object_or_404(Task, id=task_id)
    task.percentage_complete = task_percentage
    task.save()
    return JsonResponse({'status': True})


def task_put_back(request):
    reason = request.POST.get('reason')
    task_id = request.POST.get('task_id')
    task = get_object_or_404(Task, id=task_id)
    task.assigned_to = None
    task.assigned_date = None
    task.save()
    employee = get_object_or_404(Employee, user=request.user)
    backlog = Backlog.objects.create(created_for=task,
                                     created_by=employee,
                                     reason=reason)
    backlog.save()
    return JsonResponse({'status': True,
                         'message': 'Task Successfully Put Back'})


def milestone(request):
    employee = get_object_or_404(Employee, user=request.user)
    projects = employee.project_set.all()
    if request.method == 'POST':
        form = MileStoneForm(request.POST)
        if form.is_valid():
            project_id = request.POST.get('projects')
            project = get_object_or_404(Project, id=project_id)
            milestone_instance = form.save()
            project.milestones.add(milestone_instance)
    else:
        form = MileStoneForm()
    context = {
        'projects': projects,
        'form': form
    }
    return render(request, 'colaborar/milestone.html', context)


def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return JsonResponse({'status': True,
                         'message': 'Task successfully Deleted'})


def delete_project(request, id):
    project = get_object_or_404(Project, id=id)
    employee = get_object_or_404(Employee, user=request.user)
    if project.created_by == employee:
        project.delete()
        return JsonResponse({'status': True,
                             'message': 'Project Successfully Archived'})
    else:
        return JsonResponse({'status': False,
                             'message': "You Don't Have Permission To Delete The Project"})


def download_project_report(request, id):
    project = get_object_or_404(Project, id=id)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=%s.xlsx" % (
        project.name + '-' + str(datetime.now()))
    book = Workbook(response, {'in_memory': True})
    sheet_1 = book.add_worksheet('Members')
    title_style = book.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter'})
    element_style = book.add_format({
        'align': 'center',
        'valign': 'vcenter'})
    element_date_format = book.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'num_format': 'd mmm yyyy'})
    sheet_1_columns = ["ID", "First Name",
                       "Last Name", "Username", "Email", "Role"]
    first_name_col_width = last_name_col_width = username_col_width = email_col_width = role_col_width = 10
    row = 0
    for i, elem in enumerate(sheet_1_columns):
        sheet_1.write(row, i, elem, title_style)
    row += 1
    for member in project.members.all():
        sheet_1.write(row, 0, member.user.id, element_style)
        sheet_1.write(row, 1, member.user.first_name, element_style)
        sheet_1.write(row, 2, member.user.last_name, element_style)
        sheet_1.write(row, 3, member.user.username, element_style)
        sheet_1.write(row, 4, member.user.email, element_style)
        sheet_1.write(row, 5, member.role.name, element_style)
        if len(member.user.first_name) > first_name_col_width:
            first_name_col_width = len(member.user.first_name)
        if len(member.user.last_name) > last_name_col_width:
            last_name_col_width = len(member.user.last_name)
        if len(member.user.username) > username_col_width:
            username_col_width = len(member.user.username)
        if len(member.user.email) > email_col_width:
            email_col_width = len(member.user.email)
        if len(member.role.name) > role_col_width:
            role_col_width = len(member.role.name)
        row += 1
    sheet_1.set_column('A:A', 10)
    sheet_1.set_column('B:B', first_name_col_width)
    sheet_1.set_column('C:C', last_name_col_width)
    sheet_1.set_column('D:D', username_col_width)
    sheet_1.set_column('E:E', email_col_width)
    sheet_1.set_column('F:F', role_col_width)

    sheet_2 = book.add_worksheet('Task Report')
    title_text = "Tasks Summary"
    sheet_2.merge_range('A2:H2', title_text, title_style)
    row = 3
    sheet_2_columns = ['ID', 'Task Name',
                       '% Complete', 'Assigned To', 'Assigned Date',
                       'Last Updated', 'Created Date']
    for i, elem in enumerate(sheet_2_columns):
        sheet_2.write(row, i, elem, title_style)
    row += 1
    tasks = project.tasks.all().order_by('percentage_complete')
    task_name_col_width = assigned_to_col_width = 10
    for task in tasks:
        sheet_2.write(row, 0, task.id, element_style)
        sheet_2.write(row, 1, task.name, element_style)
        sheet_2.write(row, 2, task.percentage_complete, element_style)
        if task.assigned_to:
            sheet_2.write(
                row, 3, task.assigned_to.user.username, element_style)
            if len(task.assigned_to.user.username) > assigned_to_col_width:
                assigned_to_col_width = len(task.assigned_to.user.username)
        else:
            sheet_2.write(row, 3, "None", element_style)
        sheet_2.write(row, 4, task.assigned_date, element_date_format)
        sheet_2.write(row, 5, task.updated_at, element_date_format)
        sheet_2.write(row, 6, task.created_at, element_date_format)
        if len(task.name) > task_name_col_width:
            task_name_col_width = len(task.name)
        row += 1
    sheet_2.set_column('A:A', 10)
    sheet_2.set_column('B:B', task_name_col_width)
    sheet_2.set_column('C:C', 20)
    sheet_2.set_column('D:D', assigned_to_col_width + 10)
    sheet_2.set_column('E:E', 20)
    sheet_2.set_column('F:F', 20)
    sheet_2.set_column('G:G', 20)
    book.close()
    return response
