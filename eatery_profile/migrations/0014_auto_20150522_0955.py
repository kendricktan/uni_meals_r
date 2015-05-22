# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0013_auto_20150522_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_hearts',
            name='user_profile',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='location',
            name='eatery_profile',
            field=models.ForeignKey(to='eatery_profile.eatery_profile'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='user_profile',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='specials_hearts',
            name='user_profile',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_votes',
            name='eatery_profile',
            field=models.ForeignKey(to='eatery_profile.eatery_profile'),
        ),
        migrations.AlterField(
            model_name='user_votes',
            name='user_profile',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
