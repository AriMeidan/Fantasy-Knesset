from django.shortcuts import render

class indexView(generic.ListView):
    template_name = 'fknesset/index.html'
    context_object_name = 'Top 20 Knesset members'
    
    def get_queryset(self):
        return Candidtae.objects