from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from votes.models import Candidate, Party


class CreateCandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        exclude = [
                   'voters',
                   'is_knesset_member',
                   'number_of_votes'
                   ]

    def __init__(self, *args, **kwargs):
        super(CreateCandidateForm, self).__init__(*args, **kwargs)
        self.fields['party'].empty_label = _('Independent')
