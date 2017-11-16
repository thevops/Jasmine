from django.contrib import admin
from .models import Statuses, Hosts, Groups, Modules, GroupAssignment, Tasks

admin.site.site_header = 'Panel administracyjny - Jasmine'
admin.site.site_title = 'Jasmine'
admin.site.index_title = 'Panel'

@admin.register(Statuses)
class StatusesAdmin(admin.ModelAdmin):
    model = Statuses
    list_display = ('id','name','description')

@admin.register(Hosts)
class HostsAdmin(admin.ModelAdmin):
    model = Hosts
    list_display = ('id', 'dns_name', 'ip_address', 'description', 'status', 'last_seen', 'synchronization_period')
    list_display_links = ('status',)

@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    model = Groups
    list_display = ('id', 'name', 'description')

@admin.register(Modules)
class ModulesAdmin(admin.ModelAdmin):
    model = Modules
    list_display = ('id', 'name', 'description', 'configuration')

@admin.register(GroupAssignment)
class GroupAssignmentAdmin(admin.ModelAdmin):
    model = GroupAssignment
    list_display = ('id', 'host_id', 'group_id')

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    model = Tasks
    list_display = ('id', 'name', 'description', 'module', 'worker')
    list_display_links = ('module', 'worker')
    list_select_related = ('module', 'worker')


