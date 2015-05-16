# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_auto_20150516_2032'),
    ]

    operations = [
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
                ('title', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=32767)),
                ('datetime_sent', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='message_reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_id', models.IntegerField()),
                ('text', models.CharField(max_length=32767)),
                ('datetime_sent', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(to='user_profile.message')),
            ],
        ),
        migrations.CreateModel(
            name='timeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_profile', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='vote_given',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eatery_id', models.IntegerField()),
                ('is_upvoted', models.BooleanField()),
                ('datetime_voted', models.DateTimeField(auto_now_add=True)),
                ('timeline', models.ForeignKey(to='user_profile.timeline')),
            ],
        ),
        migrations.CreateModel(
            name='wall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_profile', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='wall_post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_id', models.IntegerField()),
                ('text', models.CharField(max_length=255)),
                ('datetime_pub', models.DateTimeField(auto_now_add=True)),
                ('wall', models.ForeignKey(to='user_profile.wall')),
            ],
        ),
        migrations.CreateModel(
            name='wall_post_comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_id', models.IntegerField()),
                ('text', models.CharField(max_length=255)),
                ('datetime_pub', models.DateTimeField(auto_now_add=True)),
                ('wall_post', models.ForeignKey(to='user_profile.wall_post')),
            ],
        ),
        migrations.AddField(
            model_name='food_hearted',
            name='timeline',
            field=models.ForeignKey(to='user_profile.timeline'),
        ),
        migrations.AddField(
            model_name='eatery_reviewed',
            name='timeline',
            field=models.ForeignKey(to='user_profile.timeline'),
        ),
    ]
