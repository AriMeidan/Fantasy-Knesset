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


import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


class Party(models.Model):
    name = models.CharField(_('name'), max_length=200)
    official_site = models.URLField(_('official site'), null=True, blank=True)
    facebook_page = models.URLField(_('facebook_page'), null=True, blank=True)
    wikpedia_article = models.URLField(
        _('wikipedia_article'), null=True, blank=True)
    wikpedia_url = models.URLField(_('wikipedia_url'), null=True, blank=True)
    open_k_url = models.URLField(_('open_knesset_url'), null=True, blank=True)
    logo_url = models.URLField(_('logo_url'), null=True, blank=True)

    def __unicode__(self):
        return self.name


class Candidate(models.Model):
    party = models.ForeignKey(Party,
                              verbose_name=_('party'))
    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, null=True, blank=True
    )
    name = models.CharField(_('name'), max_length=200)
    number_of_votes = models.PositiveIntegerField(default=0)
    is_knesset_member = models.BooleanField(default=False)
    personal_site = models.URLField(_('personal site'), null=True, blank=True)
    facebook_page = models.URLField(_('facebook_page'), null=True, blank=True)
    wikpedia_article = models.URLField(
        _('wikipedia_article'), null=True, blank=True)
    wikpedia_url = models.URLField(_('wikipedia_url'), null=True, blank=True)
    open_k_url = models.URLField(_('open_knesset_url'), null=True, blank=True)
    image_url = models.URLField(
        _('picture_url'), null=True, blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse('votes:candidate', args=(self.id,))

    def __unicode__(self):
        return self.name

    def vote(self, user, upvote):
        if upvote and user not in self.voters.all():
            self.voters.add(user)
            self.number_of_votes = models.F('number_of_votes') + 1
        elif not upvote and user in self.voters.all():
            self.voters.remove(user)
            self.number_of_votes = models.F('number_of_votes') - 1
        
        self.save()

        Log.log(self.pk)

    class Meta:
        ordering = ['-number_of_votes']

    def history(self):
        '''
        Returns a json with the candidate history log.
        '''

        logs = Log.objects.filter(candidate__pk=self.pk)
        fmt = "%Y-%m-%d %H:%M"
        history = [dict(timestamp=log.timestamp.strftime(fmt),
                        value=log.number_of_votes) \
                   for log in logs]

        # always add current number of votes
        history.append(dict(
            timestamp=timezone.now().strftime(fmt),
            value=self.number_of_votes)
        )

        # history normalization
        max_item = max(history, key=lambda x: x['value'])
        if max_item['value'] != 0:
            for item in history:
                item['value'] /= float(max_item['value'])

        return json.dumps(history)


class Log(models.Model):
    candidate = models.ForeignKey(Candidate)
    number_of_votes = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'candidate: {}, votes: {}, timestamp: {}' \
            .format(self.candidate.name,
                    self.number_of_votes,
                    self.timestamp.strftime('%Y-%m-%d %H:%M')
                    )

    @classmethod
    def log(cls, pk):
        c = Candidate.objects.get(pk=pk)
        cls.objects.create(candidate=c,
                           number_of_votes=c.number_of_votes)
