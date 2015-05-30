# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0018_auto_20150526_0820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food_hearts',
            old_name='date_hearted',
            new_name='datetime_hearted',
        ),
        migrations.RenameField(
            model_name='specials_hearts',
            old_name='date_hearted',
            new_name='datetime_hearted',
        ),
    ]
