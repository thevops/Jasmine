from django.conf.urls import url, include
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
]