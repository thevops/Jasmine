from django.conf.urls import url, include
from . import views

app_name = 'controller'
urlpatterns = [
    url(r'^$', views.start_view, name='start_view'),
]