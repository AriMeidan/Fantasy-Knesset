from django.contrib.auth.models import User
from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=200)
    pesonal_site = models.URLField(null=True, blank=True)
    facebook_page = models.URLField(null=True, blank=True)
    wikpedia_article = models.URLField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    voters = models.ManyToManyField(User, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def number_of_votes(self):
        return self.voters.count()
