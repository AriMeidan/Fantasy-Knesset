from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    pesonal_site = models.URLField(null=True, blank=True)
    facebook_page = models.URLField(null=True, blank=True)
    wikpedia_article = models.URLField(null=True, blank=True)
    wikpedia_url = models.URLField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    
    users = models.ManyToManyField(User, null=True, blank=True)
    
    def __unicode__(self):  
        return self.name
    
class Votes(models.Model):    
    candidate = models.ForeignKey(Candidate, related_name='candidates_voted_for', primary_key=True)
    num_of_votes = models.IntegerField()
    
    def __unicode__(self):
        return self.candidate.name
    