from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from votes.models import Candidate

class IndexView(generic.ListView):
    template_name = 'votes/index.html'
    context_object_name = 'candidate_list'
    def get_queryset(self):
        return Candidate.objects.all()[:20]   
     
class voting(generic.ListView):
    template_name = 'votes/voting.html'
    context_object_name = 'candidate_list'
    voted = 'true'
    
    def get_queryset(self):
        return Candidate.objects.all()[:20]


def register_signin(request):
    return render(request, 'votes/register_tabbed.html')

def login(request):
    return render(request, 'votes/login.html')