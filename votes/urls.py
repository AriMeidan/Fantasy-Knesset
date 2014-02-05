from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy

from votes import views

urlpatterns = patterns('',

    # Index view
    url(r'^$', views.IndexView.as_view(), name='index'),

    # Candidate details view
    url(r'^candidate/(?P<pk>\d+)/$',
        views.CandidateView.as_view(),
        name='candidate'),

    # Candidate history (AJAX)
    url(r'^candidate/(?P<pk>\d+)/history$',
        views.candidate_history,
        name='candidate_history'),

    # Searching for candidate (AJAX)
    url(r'^search/$', views.search, name='autocomplete-search'),

    # Used for single vote (AJAX)
    url(r'^vote/$', views.vote, name='vote'),

    # Used for voting in a form. POST -> redirect
    url(r'^votes/$', views.batch_vote, name='batch_vote'),

    # Accounts administration
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'votes/login.html'}, name="login"),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('votes:index')}, name="logout"),

    # Adding candidates
    url(r'^add-candidate/new/$',
        views.CreateCandidateView.as_view(),
        name='add-candidate'),
    url(r'^add-candidate/$',
        views.add_candidate_from_fb,
        name='add-from-fb'),

    # Static content pages
    url(r'^feedback/$',
        views.FeedbackView.as_view(),
        name='feedback'),
    url(r'^work-in-progress/$',
        views.WorkInProgress.as_view(),
        name='work-in-progress'),
)
