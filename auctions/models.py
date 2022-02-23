from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin

class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    startingBid = models.FloatField()
    category = models.CharField(max_length=100)
    image = models.URLField()
    currentBid = models.FloatField()


admin.site.register(Listing)
admin.site.register(User)
