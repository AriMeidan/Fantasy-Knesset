from django.contrib import admin
from votes.models import Party, Candidate, Log

# Register your models here.
admin.site.register(Party)
admin.site.register(Candidate)
admin.site.register(Log)
