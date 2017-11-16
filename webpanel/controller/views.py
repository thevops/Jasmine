# standard library
# django core
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# thrid-part modules
# this app
from .forms import HostsAddForm
from .models import Hosts

@login_required
def start_view(request):
    return render(request, 'controller/index.html',)

# ------------------ HOSTS ------------------  #

@login_required
def hosts_list_view(request):
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
            messages.error(request, 'Invalid add host form !!!')
            return redirect('controller:add_host')
    else:
        add_host_form = HostsAddForm()
        data = {
            "add_host_form": add_host_form
        }
        return render(request, 'controller/hosts/add_host.html', data)

@login_required
def edit_host_view(request, id=None):
    instance = get_object_or_404(Hosts, pk=id)
    edit_form = HostsAddForm(request.POST or None, instance=instance)
    if request.method == "POST" and edit_form.is_valid():
        edit_form.save()
        return redirect('controller:hosts_list')
    else:
        data = {
            "edit_form": edit_form
        }
        return render(request, 'controller/hosts/edit_host.html', data)
