# Generated by Django 3.2.8 on 2022-02-24 02:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20220223_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='highestBidder',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='highestBidder', to=settings.AUTH_USER_MODEL),
        ),
    ]
