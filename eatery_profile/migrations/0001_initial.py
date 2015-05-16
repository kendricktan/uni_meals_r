# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import eatery_profile.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='downvoted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_voted', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='eatery_profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=500)),
                ('pricing', models.IntegerField(choices=[(1, b'Cheap'), (2, b'Affortable'), (3, b'Moderate'), (4, b'Expensive'), (5, b'Very Expensive')])),
            ],
        ),
        migrations.CreateModel(
            name='food',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('description', models.CharField(max_length=255)),
                ('picture', models.ImageField(null=True, upload_to=eatery_profile.models.generate_directory_eatery_food, blank=True)),
                ('eatery_profile', models.ForeignKey(to='eatery_profile.eatery_profile')),
            ],
        ),
        migrations.CreateModel(
            name='location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=120)),
                ('country_long', models.CharField(max_length=30)),
                ('country_short', models.CharField(max_length=5)),
                ('state_long', models.CharField(max_length=30)),
                ('state_short', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=30)),
                ('suburb', models.CharField(max_length=30)),
                ('postal_code', models.IntegerField()),
                ('coordinates_latitude', models.DecimalField(max_digits=8, decimal_places=3)),
                ('coordinates_longitude', models.DecimalField(max_digits=8, decimal_places=3)),
                ('eatery_profile', models.OneToOneField(to='eatery_profile.eatery_profile')),
            ],
        ),
        migrations.CreateModel(
            name='opening_hours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_from', models.IntegerField(choices=[(1, b'Monday'), (2, b'Tuesday'), (3, b'Wednesday'), (4, b'Thursday'), (5, b'Friday'), (6, b'Saturday'), (7, b'Sunday')])),
                ('day_to', models.IntegerField(choices=[(1, b'Monday'), (2, b'Tuesday'), (3, b'Wednesday'), (4, b'Thursday'), (5, b'Friday'), (6, b'Saturday'), (7, b'Sunday')])),
                ('hour_from', models.TimeField()),
                ('hour_to', models.TimeField()),
                ('eatery_profile', models.ForeignKey(to='eatery_profile.eatery_profile')),
            ],
        ),
        migrations.CreateModel(
            name='reviews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('stars_given', models.IntegerField(null=True, blank=True)),
                ('review_text', models.CharField(max_length=255)),
                ('useful_count', models.IntegerField(null=True, blank=True)),
                ('not_useful_count', models.IntegerField(null=True, blank=True)),
                ('eatery_profile', models.ForeignKey(to='eatery_profile.eatery_profile')),
            ],
        ),
        migrations.CreateModel(
            name='special_days',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('opened', models.BooleanField()),
                ('hour_from', models.TimeField(null=True, blank=True)),
                ('hour_to', models.TimeField(null=True, blank=True)),
                ('eatery_profile', models.ForeignKey(to='eatery_profile.eatery_profile')),
            ],
        ),
        migrations.CreateModel(
            name='special_tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=50)),
                ('eatery_profile', models.ManyToManyField(to='eatery_profile.eatery_profile')),
            ],
        ),
        migrations.CreateModel(
            name='specials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('description', models.CharField(max_length=255)),
                ('picture', models.ImageField(null=True, upload_to=eatery_profile.models.generate_directory_eatery_specials, blank=True)),
                ('date_valid_from', models.DateField()),
                ('date_valid_to', models.DateField()),
                ('hour_valid_from', models.TimeField(null=True, blank=True)),
                ('hour_valid_to', models.TimeField(null=True, blank=True)),
                ('eatery_profile', models.ForeignKey(to='eatery_profile.eatery_profile')),
            ],
        ),
        migrations.CreateModel(
            name='tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=50)),
                ('eatery_profile', models.ManyToManyField(to='eatery_profile.eatery_profile')),
            ],
        ),
        migrations.CreateModel(
            name='upvoted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_voted', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='votes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eatery_profile', models.OneToOneField(to='eatery_profile.eatery_profile')),
            ],
        ),
        migrations.AddField(
            model_name='upvoted',
            name='votes',
            field=models.ForeignKey(to='eatery_profile.votes'),
        ),
        migrations.AddField(
            model_name='downvoted',
            name='votes',
            field=models.ForeignKey(to='eatery_profile.votes'),
        ),
    ]
