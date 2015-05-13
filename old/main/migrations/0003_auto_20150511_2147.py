# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_wall'),
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
            name='eatery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=14)),
                ('description', models.CharField(max_length=255)),
                ('pricing', models.IntegerField()),
                ('gmaps_url', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('absolute_coordinates', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='eatery_reviewed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eatery_id', models.IntegerField()),
                ('review_stars', models.IntegerField()),
                ('review_text', models.CharField(max_length=255)),
                ('datetime_reviewed', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='food',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('description', models.CharField(max_length=500)),
                ('picture', models.ImageField(null=True, upload_to=b'text', blank=True)),
                ('eatery', models.ForeignKey(to='main.eatery')),
            ],
        ),
        migrations.CreateModel(
            name='food_hearted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('food_id', models.IntegerField()),
                ('datetime_hearted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_id', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=32767)),
                ('datetime_sent', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='main.user')),
            ],
        ),
        migrations.CreateModel(
            name='message_reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_id', models.IntegerField()),
                ('text', models.CharField(max_length=32767)),
                ('datetime_sent', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(to='main.message')),
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
                ('eatery', models.ForeignKey(to='main.eatery')),
            ],
        ),
        migrations.CreateModel(
            name='reviews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('stars_given', models.IntegerField()),
                ('review_text', models.CharField(max_length=500)),
                ('useful_no', models.IntegerField()),
                ('not_useful_no', models.IntegerField()),
                ('eatery', models.ForeignKey(to='main.eatery')),
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
                ('eatery', models.ForeignKey(to='main.eatery')),
            ],
        ),
        migrations.CreateModel(
            name='special_tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=50)),
                ('eatery', models.ManyToManyField(to='main.eatery')),
            ],
        ),
        migrations.CreateModel(
            name='specials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('normal_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('description', models.CharField(max_length=500)),
                ('date_valid_from', models.DateField()),
                ('date_valid_to', models.DateField()),
                ('hour_valid_from', models.TimeField()),
                ('hour_valid_to', models.TimeField()),
                ('eatery', models.ForeignKey(to='main.eatery')),
            ],
        ),
        migrations.CreateModel(
            name='tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=50)),
                ('eatery', models.ManyToManyField(to='main.eatery')),
            ],
        ),
        migrations.CreateModel(
            name='timeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to='main.user')),
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
            name='vote_given',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eatery_id', models.IntegerField()),
                ('is_upvoted', models.BooleanField()),
                ('timeline', models.ForeignKey(to='main.timeline')),
            ],
        ),
        migrations.CreateModel(
            name='votes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eatery', models.OneToOneField(to='main.eatery')),
            ],
        ),
        migrations.CreateModel(
            name='wall_post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_id', models.IntegerField()),
                ('text', models.CharField(max_length=999)),
                ('datetime_pub', models.DateTimeField(auto_now_add=True)),
                ('wall', models.ForeignKey(to='main.wall')),
            ],
        ),
        migrations.CreateModel(
            name='wall_post_comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_id', models.IntegerField()),
                ('text', models.CharField(max_length=999)),
                ('datetime_pub', models.DateTimeField(auto_now_add=True)),
                ('wall_post', models.ForeignKey(to='main.wall_post')),
            ],
        ),
        migrations.AddField(
            model_name='upvoted',
            name='votes',
            field=models.ForeignKey(to='main.votes'),
        ),
        migrations.AddField(
            model_name='food_hearted',
            name='timeline',
            field=models.ForeignKey(to='main.timeline'),
        ),
        migrations.AddField(
            model_name='eatery_reviewed',
            name='timeline',
            field=models.ForeignKey(to='main.timeline'),
        ),
        migrations.AddField(
            model_name='downvoted',
            name='votes',
            field=models.ForeignKey(to='main.votes'),
        ),
    ]
