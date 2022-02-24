from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin



class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=100, default="comment title")
    text = models.TextField()

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    startingBid = models.FloatField()
    category = models.CharField(max_length=100)
    image = models.URLField()
    currentBid = models.FloatField()

    highestBidder = models.ForeignKey("User", on_delete=models.DO_NOTHING, null = True, related_name="highestBidder")
    creator = models.ForeignKey("User", on_delete=models.CASCADE, null=True, related_name="creator")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey("User", on_delete=models.DO_NOTHING, null=True, related_name="winner")
    comments = models.ManyToManyField(Comment, null=True)


class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, null=True)


admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Comment)



