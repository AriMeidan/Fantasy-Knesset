from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Candidate(models.Model):
    name = models.CharField(max_length=200)
    pesonal_site = models.URLField(null=True)
    facebook_page = models.URLField(null=True)
    wikpedia_article = models.URLField(null=True)
    wikpedia_url = models.URLField(null=True)
    image_url = models.URLField(null=True)
    users = models.ManyToManyField(User)
