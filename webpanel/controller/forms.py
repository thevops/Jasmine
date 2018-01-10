# -*- coding: utf-8 -*-
from django import forms
from .models import Host, Group, Module, Task, Membership
from django.db.models import Value, BooleanField

from json import loads


class HostAddForm(forms.ModelForm):
    """ Add host """
    dns_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNS'}),
                               required=True, max_length=64, label="DNS")
    ip_address = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IP Address'}),
        protocol='IPv4', required=True, label="IP Address")
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '15', 'style': 'resize:vertical;'}),
                                  required=True, label="Description")
    synchronization_period = forms.IntegerField(min_value=1, max_value=60, required=True,
                                                label="Synchronization period (min)",
                                                widget=forms.NumberInput(
                                                    attrs={'class': 'form-control', 'placeholder': '1-60'}))
    groups = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                            queryset=Group.objects.all(), label="Groups", required=False)

    class Meta:
        model = Host
        fields = ('dns_name', 'ip_address', 'description', 'synchronization_period', 'groups')


class HostEditForm(forms.ModelForm):
    """ Edit host """
    token = forms.CharField(disabled=True)
    dns_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNS'}),
                               required=True, max_length=64, label="DNS")
    ip_address = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IP Address'}),
        protocol='IPv4', required=True, label="IP Address")
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '15', 'style': 'resize:vertical;'}),
                                  required=True, label="Description")
    synchronization_period = forms.IntegerField(min_value=1, max_value=60, required=True,
                                                label="Synchronization period (min)",
                                                widget=forms.NumberInput(
                                                    attrs={'class': 'form-control', 'placeholder': '1-60'}))
    groups = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                            queryset=Group.objects.none(), label="Groups", required=False)

    class Meta:
        model = Host
        fields = ('dns_name', 'ip_address', 'description', 'synchronization_period', 'groups', 'token')

    def __init__(self, *args, **kwargs):
        """ Filtering Groups selected by Host or not """
        super(HostEditForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if instance:
            selected = instance.group_set.all()
            selected_id = [x.id for x in selected]
            not_selected = Group.objects.exclude(pk__in=selected_id)
            qs = selected | not_selected  # for concatenate two querysets
            self.fields['groups'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                                  queryset=qs, label="Groups", required=False)
            self.initial['groups'] = selected_id  # set which Groups will be 'checked'


class GroupAddForm(forms.ModelForm):
    """ Add group """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
                           required=True, max_length=64, label="Name of group")
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '5', 'style': 'resize:vertical;'}),
                                  required=True, label="Description")

    hosts = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                           queryset=Host.objects.all(), label="Hosts", required=False)

    class Meta:
        model = Group
        fields = ('name', 'description', 'hosts')


class GroupEditForm(forms.ModelForm):
    """ Add group """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
                           required=True, max_length=64, label="Name of group")
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '5', 'style': 'resize:vertical;'}),
                                  required=True, label="Description")

    hosts = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                           queryset=Host.objects.all(), label="Hosts", required=False)

    class Meta:
        model = Group
        fields = ('name', 'description', 'hosts')

    def __init__(self, *args, **kwargs):
        """ Filtering Hosts in Group or not """
        super(GroupEditForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if instance:
            selected = instance.members.all()
            selected_id = [x.id for x in selected]
            not_selected = Host.objects.exclude(pk__in=selected_id)
            qs = selected | not_selected  # for concatenate two querysets
            self.fields['hosts'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                                 queryset=qs, label="Hosts", required=False)
            self.initial['hosts'] = selected_id  # set which Groups will be 'checked'


class ModuleAddForm(forms.ModelForm):
    """ Add module """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
                           required=True, max_length=64, label="Name")
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '5', 'style': 'resize:vertical;'}),
                                  required=True, label="Description")
    configuration = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Configuration', 'rows': '5', 'style': 'resize:vertical;'}),
                                    required=True, label="Configuration")

    def clean_configuration(self):
        """ Check if configuration field is JSON formatted """
        configuration = self.cleaned_data['configuration']
        try:
            loads(configuration)
        except ValueError:
            raise forms.ValidationError("Configuration muste have JSON format !")

        return configuration

    class Meta:
        model = Module
        fields = ('name', 'description', 'configuration')


class HostTaskAddForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'If empty, it will be set to module name'}),
        required=False, max_length=64, label="Name")
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '5', 'style': 'resize:vertical;'}),
        required=False, label="Description")
    module = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                    queryset=Module.objects.all(),
                                    label="Module", required=True, empty_label=None)
    workers = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Host.objects.all(),
                                     label="Workers", required=True)
    enumeration = forms.BooleanField(label="Workers enumeration", required=False)

    class Meta:
        model = Task
        fields = ('name', 'description', 'module', 'workers', 'enumeration')

class GroupTaskAddForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'If empty, it will be set to module name'}),
        required=False, max_length=64, label="Name")
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '5', 'style': 'resize:vertical;'}),
        required=False, label="Description")
    module = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                    queryset=Module.objects.all(),
                                    label="Module", required=True, empty_label=None)
    group = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }), queryset=Group.objects.all(),
                                     label="Group", required=True, empty_label=None)
    enumeration = forms.BooleanField(label="Workers enumeration", required=False)

    class Meta:
        model = Task
        fields = ('name', 'description', 'module', 'group','enumeration')
