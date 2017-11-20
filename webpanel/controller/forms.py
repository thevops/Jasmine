# -*- coding: utf-8 -*-
from django import forms
from .models import Statuses, Hosts, Groups, Modules, GroupAssignment, Tasks

class HostsAddForm(forms.ModelForm):
    """ Add host """
    dns_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'DNS'}),
                                required=True, max_length=64, label="DNS")
    ip_address = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'IP Address'}),
                                             protocol='IPv4', required=True, label="IP Address")
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Description','rows':'5'}),
                                  required=True, label="Description")
    synchronization_period = forms.IntegerField(min_value=1, max_value=60, required=True, label="Synchronization period (min)",
                                                widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'1-60'}))

    class Meta:
        model = Hosts
        fields = ('dns_name', 'ip_address', 'description', 'synchronization_period')

class GroupsAddForm(forms.ModelForm):
    """ Add group """
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
                           required=True, max_length=64, label="Name of group")
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Description','rows':'5'}),
                                  required=True, label="Description")

    class Meta:
        model = Groups
        fields = ('name', 'description')

class ModulesAddForm(forms.ModelForm):
    """ Add modules """
    name = forms.CharField(max_length=64, required=True, label="nazwa modułu")
    descrpiton = forms.CharField(widget=forms.Textarea, required=True, label="opis")
    configration = forms.CharField(widget=forms.Textarea, required=True, label="konfiguracja")

    class Meta:
        model = Modules
        fields = ('name', 'description', 'configuration')
