from django.http import HttpResponse
from django.db.models import F
from django.views import generic
from django.shortcuts import render_to_response, redirect, render
from django.core.urlresolvers import reverse_lazy
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from votes.models import Candidate


class IndexView(generic.ListView):
    template_name = 'votes/index.html'
    context_object_name = 'candidate_list'

    def get_queryset(self):
        return Candidate.objects.all()[:20]

def index(request):
    top20 = Candidate.objects.all()[:20]
    rest100 = Candidate.objects.all()[21:120]
    context = {
               'top20' : top20,
               'rest100' : rest100
               }
    
    return render(request, 'votes/index.html', context)
 
@login_required(login_url=reverse_lazy('votes:login'))   
def batch_vote(request):   
   
    if request.method == 'POST': 
        
        batch_vote = request.POST.getlist('candidate_checkbox')
        
        for candidate_pk in batch_vote:
            candidate = Candidate.objects.get(pk=candidate_pk)
            if request.user not in candidate.voters.all():
                candidate.voters.add(request.user)
                candidate.number_of_votes = F('number_of_votes') + 1
                candidate.save()

    return redirect('votes:index')
    
    
    
    
    
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

@login_required(login_url=reverse_lazy('votes:login'))
def vote(request, candidate_pk):
    candidate = Candidate.objects.get(pk=candidate_pk)
    if request.user not in candidate.voters.all():
        candidate.voters.add(request.user)
        candidate.number_of_votes = F('number_of_votes') + 1
        candidate.save()

    return redirect('votes:index')

@login_required(login_url=reverse_lazy('votes:login'))
def unvote(request, candidate_pk):
    candidate = Candidate.objects.get(pk=candidate_pk)
    if request.user in candidate.voters.all():
        candidate.voters.remove(request.user)
        candidate.number_of_votes = F('number_of_votes') - 1
        candidate.save()

    return redirect('votes:index')
