import random

from django.http import HttpResponse
from django.db.models import F
from django.views import generic
from django.shortcuts import render_to_response, redirect, render
from django.core.urlresolvers import reverse_lazy
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from votes.models import Candidate, Party

User = get_user_model()



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
        return context


class CandidatesByPartyView(generic.ListView):
    template_name = 'votes/candidates.html'
    context_object_name = 'parties'
    model = Party


@login_required(login_url=reverse_lazy('votes:login'))
def batch_vote(request):

    if request.method == 'POST':

        batch_votes = request.POST.getlist('candidate_checkbox')

        votes_to_add = Candidate.objects.filter(pk__in=batch_votes) \
            .exclude(pk__in=request.user.candidate_set.all().
                     values('pk'))

        for candidate in votes_to_add:
            candidate.vote_by(request.user)

        votes_to_remove = request.user.candidate_set.all() \
            .exclude(pk__in=batch_votes)

        for candidate in votes_to_remove:
            candidate.unvote_by(request.user)

    return redirect('votes:index')


# for voting and unvoting
@login_required(login_url=reverse_lazy('votes:login'))
def vote(request):

    next = 'votes:index'  # temporary next view

    if request.method == 'POST':
        candidate_pk = request.POST.get('candidate_pk')
        candidate = Candidate.objects.get(pk=candidate_pk)
        method = request.POST.get('method');
        if method == 'vote':
            candidate.vote_by(request.user)
        elif method == 'unvote':
            candidate.unvote_by(request.user)

        next = request.POST.get('next')

    return redirect(next)


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
