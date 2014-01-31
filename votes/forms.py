from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from votes.models import Candidate, Party


class CreateCandidateForm(forms.ModelForm):

    party = forms.ModelChoiceField(Party.objects.all(), initial=Party.objects.get(id=14))

    class Meta:
        model = Candidate
        exclude = [
                   'voters',
                   'is_knesset_member',
                   'number_of_votes'
                   ]
