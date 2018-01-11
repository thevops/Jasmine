from django.conf.urls import url

from . import views

from . import cron

app_name = 'api'
urlpatterns = [
    url(r'^task/list/$', views.list_of_waiting_tasks, name='list_of_waiting_tasks'),
    url(r'^task/(?P<task_id>[0-9]+)/$', views.get_task, name='get_task'),
    url(r'^task/(?P<task_id>[0-9]+)/result/$', views.set_task_result, name='set_task_result'),
    url(r'^module/(?P<module_id>[0-9]+)/$', views.get_module, name='get_module'),
    url(r'^host/get_configurations/$', views.get_configurations, name='get_configurations'),
    url(r'^host/periodic_report/$', views.periodic_report, name='periodic_report'),
    # cron
    url(r'^cron/refresh/host_status/$', cron.refresh_hosts_status, name='refresh_hosts_status'),
]