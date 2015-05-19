# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0003_specials_normal_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='stars_given',
        ),
    ]
