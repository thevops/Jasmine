# standard library
# django core
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe
# thrid-part modules
# this app
from .forms import HostsAddForm, GroupsAddForm
from .models import Hosts, Groups

@login_required
def start_view(request):
    return render(request, 'controller/index.html',)

# ------------------ HOSTS ------------------  #

@login_required
def hosts_list_view(request):
    """ List all hosts in table """
    all_hosts = Hosts.objects.all()
    data = {
        "hosts": all_hosts
    }
    return render(request, 'controller/hosts/hosts_list.html', data)

@login_required
def add_host_view(request):
    """ Get parameters from HostsAddForm and save it to database. """
    if request.method == "POST":
        add_host_form = HostsAddForm(request.POST)
        if add_host_form.is_valid():
            add_host_form.save()
            messages.success(request, 'Host added to inventory.')
            return redirect('controller:add_host')
        else:
            messages.error(request, mark_safe('%s' % add_host_form.errors))  # TODO printowanie errorow
            return redirect('controller:add_host')
    else:
        add_host_form = HostsAddForm()
        data = {
            "add_host_form": add_host_form
        }
        return render(request, 'controller/hosts/add_host.html', data)

@login_required
def edit_host_view(request, id=None):
    """ Get host from database to form and allow to update data """
    instance = get_object_or_404(Hosts, pk=id)
    edit_form = HostsAddForm(request.POST or None, instance=instance)
    if request.method == "POST" and edit_form.is_valid():
        edit_form.save()
        messages.success(request, '%s updated' % edit_form.cleaned_data['dns_name'])
        return redirect('controller:hosts_list')
    else:
        data = {
            "edit_form": edit_form
        }
        return render(request, 'controller/hosts/edit_host.html', data)

@login_required
def delete_host_view(request, id=None):
    """ Get host ID and delete it """
    instance = get_object_or_404(Hosts, pk=id)
    instance.delete()
    messages.success(request, 'Host %s has been removed' % instance.dns_name)
    return redirect('controller:hosts_list')

# --------------------  Groups  ------------------------ #
@login_required
def groups_list_view(request):
    """ List all groups in table """
    all_groups = Groups.objects.all()
    data = {
        "groups": all_groups
    }
    return render(request, 'controller/groups/groups_list.html', data)

@login_required
def add_group_view(request):
    """ Get parameters from GroupAddForm and save it to database. """
    if request.method == "POST":
        add_group_form = GroupsAddForm(request.POST)
        if add_group_form.is_valid():
            add_group_form.save()
            messages.success(request, 'Group added to inventory.')
            return redirect('controller:add_group')
        else:
            messages.error(request, mark_safe('%s' % add_group_form.errors))  # TODO printowanie errorow
            return redirect('controller:add_group')
    else:
        add_group_form = GroupsAddForm()
        data = {
            "add_group_form": add_group_form
        }
        return render(request, 'controller/groups/add_group.html', data)

@login_required
def edit_group_view(request, id=None):
    """ Get group from database to form and allow to update data """
    instance = get_object_or_404(Groups, pk=id)
    edit_form = GroupsAddForm(request.POST or None, instance=instance)
    if request.method == "POST" and edit_form.is_valid():
        edit_form.save()
        messages.success(request, '%s updated' % edit_form.cleaned_data['name'])
        return redirect('controller:groups_list')
    else:
        data = {
            "edit_form": edit_form
        }
        return render(request, 'controller/groups/edit_group.html', data)

@login_required
def delete_group_view(request, id=None):
    """ Get group ID and delete it """
    instance = get_object_or_404(Groups, pk=id)
    instance.delete()
    messages.success(request, 'Group %s has been removed' % instance.name)
    return redirect('controller:groups_list')
