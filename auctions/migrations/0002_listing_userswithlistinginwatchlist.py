# Generated by Django 3.2.8 on 2022-02-23 23:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='usersWithListingInWatchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
