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


from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from votes.models import Candidate, Party


class CreateCandidateForm(forms.ModelForm):

    party = forms.ModelChoiceField(Party.objects.all(),
                                   initial=Party.objects.get(id=14),
                                   label=_('party'))

    class Meta:
        model = Candidate
        exclude = [
                   'voters',
                   'is_knesset_member',
                   'number_of_votes'
                   ]


class FacebookCreateCandidateForm(forms.Form):
    url = forms.URLField()
    party = forms.ModelChoiceField(Party.objects.all(),
                                   initial=Party.objects.get(id=14),
                                   label=_('party'))
