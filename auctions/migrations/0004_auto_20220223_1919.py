# Generated by Django 3.2.8 on 2022-02-24 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20220223_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='comments',
            field=models.ManyToManyField(to='auctions.Comment'),
        ),
    ]