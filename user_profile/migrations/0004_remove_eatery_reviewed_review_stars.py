# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_auto_20150517_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eatery_reviewed',
            name='review_stars',
        ),
    ]
