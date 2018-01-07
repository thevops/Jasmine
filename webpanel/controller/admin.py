from django.contrib import admin
from .models import HostStatus, Host, Group, Module, Task, Membership, TaskStatus

admin.site.site_header = 'Panel administracyjny - Jasmine'
admin.site.site_title = 'Jasmine'
admin.site.index_title = 'Panel'

@admin.register(HostStatus)
class HostStatusAdmin(admin.ModelAdmin):
    model = HostStatus
    list_display = ('id','name','description')

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    model = TaskStatus
    list_display = ('id','name','description')

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    model = Host
    list_display = ('id', 'token', 'dns_name', 'ip_address', 'description', 'status', 'last_seen', 'synchronization_period')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ('id', 'name', 'description')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    model = Module
    list_display = ('id', 'name', 'description', 'configuration')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    list_display = ('id', 'host', 'group')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('id', 'name', 'description', 'module', 'worker', 'results', 'timestamp','parameters')
    list_display_links = ('id',)


