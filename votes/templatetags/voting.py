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


from django import template

register = template.Library()


@register.filter
def voted_for(user, candidate):
    if not user.is_authenticated():
        return False

    return candidate.voters.filter(id=user.id).exists()


@register.filter
def button_value(user, candidate):
    if candidate.voters.filter(id=user.id).exists():
    	return 0
    return 1
