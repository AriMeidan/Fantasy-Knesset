from django.conf.urls import patterns, url

from votes import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.register_signin, name='register'),
    url(r'^login/$', views.login, name='login'),
)