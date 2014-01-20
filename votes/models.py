from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Party(models.Model):
    name = models.CharField(max_length=200)
    official_site = models.URLField(null=True, blank=True)
    facebook_page = models.URLField(null=True, blank=True)
    wikpedia_article = models.URLField(null=True, blank=True)
    wikpedia_url = models.URLField(null=True, blank=True)
    open_k_url = models.URLField(null=True, blank=True)
    logo_url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Candidate(models.Model):
    party = models.ForeignKey(Party, null=True, blank=True)
    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, null=True, blank=True
    )
    name = models.CharField(max_length=200)
    number_of_votes = models.PositiveIntegerField(default=0)
    is_knesset_member = models.BooleanField(default=False)
    pesonal_site = models.URLField(null=True, blank=True)
    facebook_page = models.URLField(null=True, blank=True)
    wikpedia_article = models.URLField(null=True, blank=True)
    wikpedia_url = models.URLField(null=True, blank=True)
    open_k_url = models.URLField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('votes:candidate', args=(self.id,))

    def __unicode__(self):
        return self.name

    def vote_by(self, user):
        if user not in self.voters.all():
            self.voters.add(user)
            self.number_of_votes = models.F('number_of_votes') + 1
            self.save()

            Log.log(self.pk)

    def unvote_by(self, user):
        if user in self.voters.all():
            self.voters.remove(user)
            self.number_of_votes = models.F('number_of_votes') - 1
            self.save()

            Log.log(self.pk)

    class Meta:
        ordering = ['-number_of_votes']


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
