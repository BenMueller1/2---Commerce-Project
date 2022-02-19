from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    startingBid = models.FloatField()
    category = models.CharField(max_length=100)
    image = models.URLField()
