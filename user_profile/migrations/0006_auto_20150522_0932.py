# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_specials_hearted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eatery_reviewed',
            name='timeline',
        ),
        migrations.RemoveField(
            model_name='food_hearted',
            name='timeline',
        ),
        migrations.RemoveField(
            model_name='specials_hearted',
            name='timeline',
        ),
        migrations.RemoveField(
            model_name='timeline',
            name='user_profile',
        ),
        migrations.RemoveField(
            model_name='vote_given',
            name='timeline',
        ),
        migrations.DeleteModel(
            name='eatery_reviewed',
        ),
        migrations.DeleteModel(
            name='food_hearted',
        ),
        migrations.DeleteModel(
            name='specials_hearted',
        ),
        migrations.DeleteModel(
            name='timeline',
        ),
        migrations.DeleteModel(
            name='vote_given',
        ),
    ]
