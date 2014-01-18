from django.contrib import admin
from votes.models import Candidate, Log

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Log)
