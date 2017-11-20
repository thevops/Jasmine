from django.conf.urls import url, include
from . import views

app_name = 'controller'
urlpatterns = [
    url(r'^$', views.start_view, name='start_view'),
    # --- Host --- #
    url(r'^inventory/host/list/$', views.hosts_list_view, name='hosts_list'),
    url(r'^inventory/host/add/$', views.add_host_view, name='add_host'),
    url(r'^inventory/host/edit/(?P<id>\d+)/$', views.edit_host_view, name='edit_host'),
    url(r'^inventory/host/delete/(?P<id>\d+)/$', views.delete_host_view, name='delete_host'),
    # --- Group --- #
    url(r'^inventory/group/list/$', views.groups_list_view, name='groups_list'),
    url(r'^inventory/group/add/$', views.add_group_view, name='add_group'),
    url(r'^inventory/group/edit/(?P<id>\d+)/$', views.edit_group_view, name='edit_group'),
    url(r'^inventory/group/delete/(?P<id>\d+)/$', views.delete_group_view, name='delete_group'),
]