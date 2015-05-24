# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0016_reviews_usefulness'),
    ]

    operations = [
        migrations.AddField(
            model_name='eatery_profile',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 24, 22, 42, 46, 622000), auto_now_add=True),
            preserve_default=False,
        ),
    ]
