# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eatery_profile', '0010_auto_20150521_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_votes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_voted', models.DateField(auto_now_add=True)),
                ('is_upvoted', models.BooleanField()),
                ('eatery_profile', models.OneToOneField(to='eatery_profile.eatery_profile')),
                ('user_profile', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='downvoted',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='upvoted',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='votes',
            name='eatery_profile',
        ),
        migrations.RemoveField(
            model_name='food_hearts',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='specials_hearts',
            name='user',
        ),
        migrations.AddField(
            model_name='food_hearts',
            name='user_profile',
            field=models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviews',
            name='user_profile',
            field=models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specials_hearts',
            name='user_profile',
            field=models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='food',
            name='food_hearts',
        ),
        migrations.AddField(
            model_name='food',
            name='food_hearts',
            field=models.ForeignKey(default=1, to='eatery_profile.food_hearts'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='specials',
            name='specials_hearts',
        ),
        migrations.AddField(
            model_name='specials',
            name='specials_hearts',
            field=models.ForeignKey(default=1, to='eatery_profile.specials_hearts'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='downvoted',
        ),
        migrations.DeleteModel(
            name='upvoted',
        ),
        migrations.DeleteModel(
            name='votes',
        ),
    ]
