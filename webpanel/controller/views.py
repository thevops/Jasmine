# standard library
# django core
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe
# thrid-part module
# this app
from .models import Host, Group, Membership, Module, Task, HostStatus, TaskStatus
from .forms import HostAddForm, HostEditForm,  GroupAddForm, GroupEditForm, ModuleAddForm, HostTaskAddForm, GroupTaskAddForm

@login_required
def start_view(request):
    return render(request, 'controller/index.html',)

# --------------------------------------------------- HOSTS ------------------  #

@login_required
def host_list_view(request):
    """ List all host in table """
    all_hosts = Host.objects.all()
    data = {
        "hosts": all_hosts
    }
    return render(request, 'controller/host/list.html', data)

@login_required
def host_add_view(request):
    """ Get parameters from HostsAddForm and save it to database. """
    if request.method == "POST":
        host_add_form = HostAddForm(request.POST)
        if host_add_form.is_valid():
            groups = host_add_form.cleaned_data['groups']
            host_obj = host_add_form.save()
            # create Membership host -> many group
            Membership.bulk_save_host(host_obj=host_obj, groups_name=groups)
            messages.success(request, 'Host added to inventory.')
            return redirect('controller:host_add')
        else:
            messages.error(request, mark_safe('%s' % host_add_form.errors))  # TODO printowanie errorow
            return redirect('controller:host_add')
    else:
        host_add_form = HostAddForm()
        data = {
            "add_host_form": host_add_form
        }
        return render(request, 'controller/host/add.html', data)

@login_required
def host_edit_view(request, pk=None):
    """ Get host from database to form and allow to update data """
    instance = get_object_or_404(Host, pk=pk)
    edit_form = HostEditForm(request.POST or None, instance=instance)
    if request.method == "POST" and edit_form.is_valid():
        groups = edit_form.cleaned_data['groups']  # get selected group
        host_obj = edit_form.save()
        Membership.bulk_save_host(host_obj=host_obj, groups_name=groups)  # create membership
        messages.success(request, '%s updated' % edit_form.cleaned_data['dns_name'])
        return redirect('controller:host_list')
    else:
        data = {
            "edit_form": edit_form
        }
        return render(request, 'controller/host/edit.html', data)

@login_required
def host_delete_view(request, pk=None):
    """ Get host ID and delete it """
    instance = get_object_or_404(Host, pk=pk)
    instance.delete()
    messages.success(request, 'Host %s has been removed' % instance.dns_name)
    return redirect('controller:host_list')

# ---------------------------------------------------  GROUPS  ------------------------ #
@login_required
def group_list_view(request):
    """ List all group in table """
    all_groups = Group.objects.all()
    data = {
        "groups": all_groups
    }
    return render(request, 'controller/group/list.html', data)

@login_required
def group_add_view(request):
    """ Get parameters from GroupAddForm and save it to database. """
    if request.method == "POST":
        group_add_form = GroupAddForm(request.POST)
        if group_add_form.is_valid():
            hosts = group_add_form.cleaned_data['hosts']
            group_obj = group_add_form.save()
            # create Membership host -> many group
            Membership.bulk_save_group(hosts_name=hosts, group_obj=group_obj)
            messages.success(request, 'Group added to inventory.')
            return redirect('controller:group_add')
        else:
            messages.error(request, mark_safe('%s' % group_add_form.errors))  # TODO printowanie errorow
            return redirect('controller:group_add')
    else:
        group_add_form = GroupAddForm()
        data = {
            "add_group_form": group_add_form
        }
        return render(request, 'controller/group/add.html', data)

@login_required
def group_edit_view(request, pk=None):
    """ Get group from database to form and allow to update data """
    instance = get_object_or_404(Group, pk=pk)
    edit_form = GroupEditForm(request.POST or None, instance=instance)
    if request.method == "POST" and edit_form.is_valid():
        hosts = edit_form.cleaned_data['hosts']
        group = edit_form.save()
        Membership.bulk_save_group(hosts_name=hosts, group_obj=group)
        messages.success(request, '%s updated' % edit_form.cleaned_data['name'])
        return redirect('controller:group_list')
    else:
        data = {
            "edit_form": edit_form
        }
        return render(request, 'controller/group/edit.html', data)

@login_required
def group_delete_view(request, pk=None):
    """ Get group ID and delete it """
    instance = get_object_or_404(Group, pk=pk)
    instance.delete()
    messages.success(request, 'Group %s has been removed' % instance.name)
    return redirect('controller:group_list')


# ---------------------------------------------------  MODULES  ------------------------ #

@login_required
def module_list_view(request):
    all_modules = Module.objects.all()
    data = {
        "modules": all_modules,
    }
    return render(request, 'controller/module/list.html', data)

@login_required
def module_add_view(request):
    """ Get parameters from ModuleAddForm and save it to database. """
    if request.method == "POST":
        module_add_form = ModuleAddForm(request.POST)
        if module_add_form.is_valid():
            module_add_form.save()
            messages.success(request, 'Module added to inventory.')
            return redirect('controller:module_add')
        else:
            messages.error(request, mark_safe('%s' % module_add_form.errors))  # TODO printowanie errorow
            return redirect('controller:module_add')
    else:
        module_add_form = ModuleAddForm()
        data = {
            "add_module_form": module_add_form
        }
        return render(request, 'controller/module/add.html', data)

@login_required
def module_edit_view(request, pk=None):
    """ Get module from database to form and allow to update data """
    instance = get_object_or_404(Module, pk=pk)
    edit_form = ModuleAddForm(request.POST or None, instance=instance)
    if request.method == "POST" and edit_form.is_valid():
        edit_form.save()
        messages.success(request, '%s updated' % edit_form.cleaned_data['name'])
        return redirect('controller:module_list')
    else:
        data = {
            "edit_form": edit_form
        }
        return render(request, 'controller/module/edit.html', data)

@login_required
def module_delete_view(request, pk=None):
    """ Get module ID and delete it """
    instance = get_object_or_404(Module, pk=pk)
    instance.delete()
    messages.success(request, 'Module %s has been removed' % instance.name)
    return redirect('controller:module_list')

# ---------------------------------------------------  TASKS  ------------------------ #

@login_required
def task_list_all_view(request):
    tasks = Task.objects.all()
    data = {
        "tasks": tasks,
        "title": "All tasks list",
    }
    return render(request, 'controller/task/list.html', data)

@login_required
def task_list_completed_view(request):
    complete_status = TaskStatus.objects.get(name="completed")
    tasks = Task.objects.filter(status=complete_status)
    data = {
        "tasks": tasks,
        "title": "Completed tasks list",
    }
    return render(request, 'controller/task/list.html', data)

@login_required
def task_list_in_progress_view(request):
    inprogress_status = TaskStatus.objects.get(name="in progress")
    tasks = Task.objects.filter(status=inprogress_status)
    data = {
        "tasks": tasks,
        "title": "In progress tasks list",
    }
    return render(request, 'controller/task/list.html', data)

@login_required
def task_list_victorious_view(request):
    inprogress_status = TaskStatus.objects.get(name="victorious")
    tasks = Task.objects.filter(status=inprogress_status)
    data = {
        "tasks": tasks,
        "title": "In progress tasks list",
    }
    return render(request, 'controller/task/list.html', data)

@login_required
def task_host_add_view(request):
    """ Get parameters from HostTaskAddForm and save it to database. """
    if request.method == "POST":
        host_task_add_form = HostTaskAddForm(request.POST)
        if host_task_add_form.is_valid():
            name = host_task_add_form.cleaned_data['name']
            description = host_task_add_form.cleaned_data['description']
            module = host_task_add_form.cleaned_data['module']
            workers = host_task_add_form.cleaned_data['workers']
            parameters = host_task_add_form.cleaned_data['parameters']
            Task.bulk_save(name, description, module, workers, parameters,
                           host_task_add_form.cleaned_data['enumeration'])
            messages.success(request, 'Task added to queue.')
            return redirect('controller:task_host_add')
        else:
            messages.error(request, mark_safe('%s' % host_task_add_form.errors))  # TODO printowanie errorow
            return redirect('controller:task_host_add')
    else:
        host_task_add_form = HostTaskAddForm()
        data = {
            "host_task_add_form": host_task_add_form
        }
        return render(request, 'controller/task/add_for_host.html', data)

@login_required
def group_host_add_view(request):
    """ Get parameters from HostTaskAddForm and save it to database. """
    if request.method == "POST":
        group_task_add_form = GroupTaskAddForm(request.POST)
        if group_task_add_form.is_valid():
            name = group_task_add_form.cleaned_data['name']
            description = group_task_add_form.cleaned_data['description']
            module = group_task_add_form.cleaned_data['module']
            group_name = group_task_add_form.cleaned_data['group']
            group = Group.objects.filter(name=group_name).first()  # take Group object
            workers = group.members.all()  # find all members of group
            parameters = group_task_add_form.cleaned_data['parameters']
            Task.bulk_save(name, description, module, workers, parameters,
                           group_task_add_form.cleaned_data['enumeration'])  # for every member add task
            messages.success(request, 'Task added to queue.')
            return redirect('controller:group_host_add')
        else:
            messages.error(request, mark_safe('%s' % group_task_add_form.errors))  # TODO printowanie errorow
            return redirect('controller:group_host_add')
    else:
        group_task_add_form = GroupTaskAddForm()
        data = {
            "group_task_add_form": group_task_add_form
        }
        return render(request, 'controller/task/add_for_group.html', data)

@login_required
def task_delete_view(request, pk=None):
    """ Get task ID and delete it """
    instance = get_object_or_404(Task, pk=pk)
    instance.delete()
    messages.success(request, 'Task %s has been removed' % instance.name)
    return redirect('controller:task_list_all')

@login_required
def task_multidelete_view(request):
    to_delete = request.POST.getlist('to_delete[]')
    for i in to_delete:
        Task.objects.get(pk=i).delete()
    return redirect('controller:task_list_all')

@login_required
def task_show_view(request, pk=None):
    task = get_object_or_404(Task, pk=pk)
    data = {
        "task": task
    }
    return render(request, 'controller/task/show.html', data)

@login_required
def task_restart_view(request, pk=None):
    task = get_object_or_404(Task, pk=pk)
    stat = TaskStatus.objects.get(name="in queue")
    task.status = stat
    task.save()
    return redirect('controller:task_list_all')

# ----------------------------------------------------------------------------------

@login_required
def open_terminal(request):
    terminal_addr = "https://" + request.META.get('HTTP_HOST').split(":")[0] + ":57575"
    return redirect(terminal_addr)
