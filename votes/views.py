from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views import generic

from votes.models import Candidate


class IndexView(generic.ListView):
    template_name = 'votes/index.html'
    context_object_name = 'candidate_list'

    def get_queryset(self):
        return Candidate.objects.all()[:20]


def register(request):
	if request.method == 'GET':
		return render_to_response('votes/register.html')
	if request.method == 'POST':
		return HttpResponse("in post method")
	# name = request.POST.get('name')
	# return HttpResponse("name=" + name)

def login(request):
	if request.method == 'GET':
		return render_to_response('votes/login.html')
	if request.method == 'POST':
		return HttpResponse("in post method")
	# name = request.POST.get('name')
	# return HttpResponse("name=" + name)

def logout(request):
	return redirect('votes:index')
