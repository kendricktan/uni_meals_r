# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0019_auto_20150530_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_votes',
            name='datetime_voted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
