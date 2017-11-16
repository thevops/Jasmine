from django.conf.urls import url, include
from . import views

app_name = 'controller'
urlpatterns = [
    url(r'^$', views.start_view, name='start_view'),
    # --- Host --- #
    url(r'^inventory/add_host/$', views.add_host_view, name='add_host'),
    url(r'^inventory/hosts_list/$', views.hosts_list_view, name='hosts_list'),
    url(r'^inventory/edit_host/(?P<id>\d+)/$', views.edit_host_view, name='edit_host'),
]