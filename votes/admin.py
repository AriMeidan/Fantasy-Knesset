'''
Copyright 2014 Ari Meidan and Tom Gurion

This file is part of "Games of Knesset".

"Games of Knesset" is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"Games of Knesset" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with "Games of Knesset".  If not, see <http://www.gnu.org/licenses/>.
'''


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
