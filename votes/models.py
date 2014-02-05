import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.validators import URLValidator


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
        history = []
        fmt = "%Y-%m-%d %H:%M"
        for log in logs:
            timestamp = log.timestamp.strftime(fmt)
            value = log.number_of_votes
            history.append(dict(timestamp=timestamp, value=value))

        # always add current number of votes
        timestamp = timezone.now().strftime(fmt)
        value = self.number_of_votes
        history.append(dict(timestamp=timestamp, value=value))

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
