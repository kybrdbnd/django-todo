from django import forms
from django.forms import TextInput, PasswordInput
from django.utils.translation import ugettext_lazy as _
from .models import (Project, Company, Profile)


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


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name',)
        widgets = {
            'first_name': TextInput(attrs={
                'placeholder': 'Enter Your First Name'
            }),
            'last_name': TextInput(attrs={
                'placeholder': 'Enter Your Last Name'
            })
        }


class AcceptInvitationForm(forms.ModelForm):
    password = forms.CharField()
    confirm_password = forms.CharField()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name',)
        widgets = {
            'first_name': TextInput(attrs={
                'placeholder': 'Enter Your First Name'
            }),
            'last_name': TextInput(attrs={
                'placeholder': 'Enter Your Last Name'
            }),
            'password': PasswordInput(),
            'confirm_password': PasswordInput()
        }
