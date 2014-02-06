from django.contrib import admin
from votes.models import Party, Candidate, Log
from django.contrib.auth.models import Group

#----------------------------------------------------------
#   VOTES MODELS ADMIN
#----------------------------------------------------------

admin.site.register(Party)
admin.site.register(Candidate)
admin.site.register(Log)


#----------------------------------------------------------
#   CUSTOM USER ADMIN
#----------------------------------------------------------

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# module scooped moderator group
moderators_group, created = Group.objects.get_or_create(name='moderators')


def make_moderator(modeladmin, request, queryset):
    '''
    Custom admin action - add user to the group "moderators".
    '''

    for user in queryset.all():
        user.groups.add(moderators_group)


def disable_moderator(modeladmin, request, queryset):
    '''
    Custom admin action - remove user from the group "moderators".
    '''

    for user in queryset.all():
        user.groups.remove(moderators_group)


class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('moderator',)
    actions = [make_moderator, disable_moderator]


    def moderator(self, user):
        '''
        Returns whether the user is moderator.
        '''
        
        if moderators_group in user.groups.all():
            return True
        else:
            return False

    moderator.boolean = True


admin.site.register(get_user_model(), MyUserAdmin)
