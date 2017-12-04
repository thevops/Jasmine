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
]