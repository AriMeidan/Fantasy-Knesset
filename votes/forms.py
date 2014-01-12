from django import forms
from django.core.exceptions import ValidationError

from votes.models import Candidate, Party


class CreateCandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        exclude = [
                   'voters',
                   'is_knesset_member',
                   'number_of_votes'
                   ]
