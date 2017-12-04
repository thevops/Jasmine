from django.contrib import admin
from .models import Statuse, Host, Group, Module, Task, Membership

admin.site.site_header = 'Panel administracyjny - Jasmine'
admin.site.site_title = 'Jasmine'
admin.site.index_title = 'Panel'

@admin.register(Statuse)
class StatusesAdmin(admin.ModelAdmin):
    model = Statuse
    list_display = ('id','name','description')

@admin.register(Host)
class HostsAdmin(admin.ModelAdmin):
    model = Host
    list_display = ('id', 'dns_name', 'ip_address', 'description', 'status', 'last_seen', 'synchronization_period')

@admin.register(Group)
class GroupsAdmin(admin.ModelAdmin):
    model = Group
    list_display = ('id', 'name', 'description')

@admin.register(Module)
class ModulesAdmin(admin.ModelAdmin):
    model = Module
    list_display = ('id', 'name', 'description', 'configuration')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    list_display = ('id', 'host', 'group')

@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('id', 'name', 'description', 'module', 'worker')
    list_display_links = ('module', 'worker')
    list_select_related = ('module', 'worker')


