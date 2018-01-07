from django.conf.urls import url, include
from . import views

app_name = 'controller'
urlpatterns = [
    url(r'^$', views.start_view, name='start_view'),
    # --- Host --- #
    url(r'^inventory/host/list/$', views.host_list_view, name='host_list'),
    url(r'^inventory/host/add/$', views.host_add_view, name='host_add'),
    url(r'^inventory/host/edit/(?P<pk>\d+)/$', views.host_edit_view, name='host_edit'),
    url(r'^inventory/host/delete/(?P<pk>\d+)/$', views.host_delete_view, name='host_delete'),
    # --- Group --- #
    url(r'^inventory/group/list/$', views.group_list_view, name='group_list'),
    url(r'^inventory/group/add/$', views.group_add_view, name='group_add'),
    url(r'^inventory/group/edit/(?P<pk>\d+)/$', views.group_edit_view, name='group_edit'),
    url(r'^inventory/group/delete/(?P<pk>\d+)/$', views.group_delete_view, name='group_delete'),
    # --- Module --- #
    url(r'^inventory/module/list/$', views.module_list_view, name='module_list'),
    url(r'^inventory/module/add/$', views.module_add_view, name='module_add'),
    url(r'^inventory/module/edit/(?P<pk>\d+)/$', views.module_edit_view, name='module_edit'),
    url(r'^inventory/module/delete/(?P<pk>\d+)/$', views.module_delete_view, name='module_delete'),
    # --- Task --- #
    url(r'^task/list/all/$', views.task_list_all_view, name='task_list_all'),
    url(r'^task/list/completed/$', views.task_list_completed_view, name='task_list_completed'),
    url(r'^task/list/all/inprogress/$', views.task_list_in_progress_view, name='task_list_in_progress'),
    url(r'^task/list/all/victorious/$', views.task_list_victorious_view, name='task_list_victorious'),
    url(r'^task/add/host/$', views.task_host_add_view, name='task_host_add'),
    url(r'^task/add/group/$', views.group_host_add_view, name='group_host_add'),
    url(r'^task/delete/(?P<pk>\d+)/$', views.task_delete_view, name='task_delete'),
    url(r'^task/(?P<pk>\d+)/$', views.task_show_view, name='task_show'),
    url(r'^task/multidelete/$', views.task_multidelete_view, name='task_multidelete'),
]