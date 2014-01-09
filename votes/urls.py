from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy


from votes import views

urlpatterns = patterns('',

    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^candidates/$', views.CandidatesByPartyView.as_view(),
        name='candidates'
    ),
    
    #used for voting in a form
    url(r'^votes/$', views.batch_vote, name='batch_vote'),

    url(r'^account/register/$', views.register, name='register'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'votes/login.html'}, name="login"),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('votes:index')}, name="logout"),

    url(r'^vote/(?P<candidate_pk>\d+)/$', views.vote, name='vote'),
    url(r'^unvote/(?P<candidate_pk>\d+)/$', views.unvote, name='unvote'),

    url(r'^add-candidate/$', views.CreateCandidateView.as_view(), name='add-candidate'),

)
