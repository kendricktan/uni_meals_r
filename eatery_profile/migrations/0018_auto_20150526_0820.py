# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0017_eatery_profile_datetime_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='not_useful_count',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='useful_count',
        ),
        migrations.AddField(
            model_name='reviews',
            name='datetime_pub',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 26, 8, 20, 57, 645000), auto_now_add=True),
            preserve_default=False,
        ),
    ]
