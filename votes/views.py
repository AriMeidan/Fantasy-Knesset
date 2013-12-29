from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from votes.models import Candidate


class IndexView(generic.ListView):
    template_name = 'votes/index.html'
    context_object_name = 'candidate_list'

    def get_queryset(self):
        return Candidate.objects.all()[:20]


def register(request):

    if request.method == 'GET':
        context = {}
        context.update(csrf(request))
        return render_to_response('votes/register.html', context)

    if request.method == 'POST':

        # extract form parameters
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # create and save the user to the db
        user = User.objects.create_user(username, email, password)
        user.save()

        # authenticate the user
        user = authenticate(username=username, password=password)

        # log the user in
        login(request, user)

        return redirect('votes:index')
