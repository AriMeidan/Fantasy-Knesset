'''
Copyright 2014 Ari Meidan and Tom Gurion

This file is part of "Games of Knesset".

"Games of Knesset" is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"Games of Knesset" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with "Games of Knesset".  If not, see <http://www.gnu.org/licenses/>.
'''

import json
import random
import re

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import (login_required,
                                            permission_required)
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.decorators import method_decorator
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.views import generic
from open_facebook.api import OpenFacebook
from open_facebook.exceptions import ParameterException

from votes.forms import (CreateCandidateForm,
                         FacebookCreateCandidateForm)
from votes.models import Candidate


User = get_user_model()


#----------------------------------------------------------
#       CUSTOM DECORATORS
#----------------------------------------------------------

def login_required_ajax(function=None, redirect_field_name=None):
    """
    Just make sure the user is authenticated to access a certain ajax
    view.

    Otherwise return a HttpResponse 401 - authentication required -
    instead of the 302 redirect of the original Django decorator.

    Solution from: http://stackoverflow.com/a/10031220/1224456
    """

    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(status=401)
        return _wrapped_view

    if function:
        return _decorator(function)
    return _decorator


#----------------------------------------------------------
#       MAIN VIEWS
#----------------------------------------------------------

class IndexView(generic.TemplateView):
    template_name = 'votes/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['top20'] = sorted(Candidate.objects.all()[:20],
                                  key=lambda x: random.random()
                                  )
        context['rest100'] = sorted(Candidate.objects.all()[20:120],
                                    key=lambda x: x.name
                                    )
        context['fake5in'] = sorted(context['top20'],
                                    key=lambda x: random.random()
                                   )[:5]
        context['fake5out'] = sorted(context['rest100'],
                                     key=lambda x: random.random()
                                    )[:5]

        # adding faked time in top20
        for cand in context['top20']:
            cand.weeks = random.randrange(4) + 1

        return context


class CandidateView(generic.DetailView):
    model = Candidate


#----------------------------------------------------------
#       STATIC CONTENT VIEWS
#----------------------------------------------------------

class FeedbackView(generic.TemplateView):
    template_name = 'votes/feedback.html'


class WorkInProgress(generic.TemplateView):
    template_name = 'votes/work_in_progress.html'


#----------------------------------------------------------
#       DATA CREATION VIEWS (POSTS -> redirect)
#----------------------------------------------------------

# batch voting from index view
@login_required(login_url=reverse_lazy('votes:login'))
def batch_vote(request):

    if request.method == 'POST':

        batch_votes = request.POST.getlist('candidate_checkbox')

        votes_to_add = Candidate.objects.filter(pk__in=batch_votes) \
            .exclude(pk__in=request.user.candidate_set.all().
                     values('pk'))

        for candidate in votes_to_add:
            candidate.vote(request.user, upvote=True)

        votes_to_remove = request.user.candidate_set.all() \
            .exclude(pk__in=batch_votes)

        for candidate in votes_to_remove:
            candidate.vote(request.user, upvote=False)

    return redirect('votes:index')


# creating a candidate manually
class CreateCandidateView(generic.CreateView):
    model = Candidate
    form_class = CreateCandidateForm

    @method_decorator(permission_required('votes.add_candidate'))
    def dispatch(self, *args, **kwargs):
        return super(CreateCandidateView, self). \
            dispatch(*args, **kwargs)


# creating a candidate from facebook page
@permission_required('votes.add_candidate')
def add_candidate_from_fb(request):

    if request.method == 'POST':
        form = FacebookCreateCandidateForm(request.POST)
        if form.is_valid():
            fb = OpenFacebook()
            # fb_url = request.POST.get('fb_page')
            fb_url = form.cleaned_data['url']
            # party = Party.objects.get(id=request.POST.get('party'))
            party = form.cleaned_data['party']
            try:
                res = fb.get(fb_url, fields='name, website, picture.type(large)')
                sites = res.get('website', None).split(' ')
                for site in sites:
                    try:
                        if site == '':
                            continue
                        URLValidator(site)
                        val = site
                        break
                    except ValidationError as e:
                        print site, "is not a valid url"
                        continue

                # add another validation
                c = Candidate(name=res['name'],
                              image_url=res['picture']['data']['url'],
                              personal_site=val,
                              facebook_page=fb_url,
                              party=party)
                c.save()
                messages.info(request, "Added Successfully")
                return redirect(c.get_absolute_url())
            except ParameterException as e:
                messages.error(request, e.message)
    else:
        form = FacebookCreateCandidateForm()

    return render(request,
                  'votes/candidate_fb_form.html',
                  {'form': form})


#----------------------------------------------------------
#       AJAX / JSON VIEWS
#----------------------------------------------------------

# get candidate history json
def candidate_history(request, pk):
    c = Candidate.objects.get(pk=pk)
    return HttpResponse(c.history())


# for vote and unvote using AJAX
@login_required_ajax
def vote(request):

    results = dict(success=False)

    if request.method == 'POST':
        candidate = Candidate.objects.get(
            pk=request.POST.get('candidate_pk')
        )
        upvote = int(request.POST.get('upvote'))
        candidate.vote(request.user, upvote=upvote)
        results['success'] = True

    return HttpResponse(json.dumps(results))


# for searching via autocomplete
def search(request):
        search_str = request.GET.get('item')
        str_to_match = re.compile(r'^'+search_str+'|([\u05D0-\u05EA]+(\s|[^\u05D0-\u05EA])+)'+search_str)
        results = Candidate.objects.filter(name__regex=str_to_match.pattern)
        data = []
        for candidate in results:
            url = candidate.get_absolute_url()
            name = candidate.name
            data.append(dict(name=name, url=url))

        return HttpResponse(json.dumps(data))


#----------------------------------------------------------
#       ACCOUNTS MANAGEMENT
#----------------------------------------------------------

def register(request):

    error = None

    if request.method == 'POST':

        # extract form parameters
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # continue only if the username is unique
        if len(User.objects.filter(username=username)) == 0:

            # create and save the user to the db
            user = User.objects.create_user(username, email, password)
            user.save()

            # authenticate the user, log in and redirect
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('votes:index')

        # if username is not unique set the error
        error = 'Username already exist'

    context = dict(error=error)
    context.update(csrf(request))
    return render_to_response('votes/register.html', context)
