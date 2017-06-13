from django import forms
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from .models import (Project, Company)


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
