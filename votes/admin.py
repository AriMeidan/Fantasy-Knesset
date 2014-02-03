from django.contrib import admin
from votes.models import Party, Candidate, Log

# Register your models here.
admin.site.register(Party)
admin.site.register(Candidate)
admin.site.register(Log)

# adding costum user admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

admin.site.register(get_user_model(), UserAdmin)