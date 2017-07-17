from django import forms
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from .models import (Project, Company, Profile, Employee, Role, Milestone)
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)
        labels = {
            'name': _('Company Name:'),
        }
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Enter Company Name:'
            })
        }

    def signup(self, request, user):
        company = Company()
        company_name = self.cleaned_data['name']
        company.owner = user
        company.name = company_name
        company.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        employee = Employee.objects.create(user=user)
        employee.save()
        company.employees.add(employee)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': TextInput(attrs={
                'placeholder': 'Enter Your First Name'
            }),
            'last_name': TextInput(attrs={
                'placeholder': 'Enter Your Last Name'
            })
        }


class RoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(Role.objects.all(), empty_label=None)

    class Meta:
        model = Employee
        fields = ['role']


class MileStoneForm(forms.ModelForm):
    # projects = forms.MultipleChoiceField()

    class Meta:
        model = Milestone
        fields = ['name', 'description', 'start_date', 'end_date']
