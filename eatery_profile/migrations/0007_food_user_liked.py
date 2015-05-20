# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0006_auto_20150520_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='user_liked',
            field=models.BooleanField(default=False),
        ),
    ]
