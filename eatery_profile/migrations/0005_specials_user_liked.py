# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0004_remove_reviews_stars_given'),
    ]

    operations = [
        migrations.AddField(
            model_name='specials',
            name='user_liked',
            field=models.NullBooleanField(),
        ),
    ]
