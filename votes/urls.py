from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from votes import views

urlpatterns = patterns('',

    url(r'^$', views.IndexView.as_view(), name='index'),

	url(r'^account/register/$', views.register, name='register'),

	url(r'^account/login/$', views.login, name='login'),

    url(r'^account/logout/do$', views.logout, name='logout'),
)
