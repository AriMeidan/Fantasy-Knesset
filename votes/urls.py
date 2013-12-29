from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy


from votes import views

urlpatterns = patterns('',

    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^account/register/$', views.register, name='register'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'votes/login.html'}, name="login"),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('votes:index')}, name="logout"),
)
