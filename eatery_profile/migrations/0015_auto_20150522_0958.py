# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0014_auto_20150522_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='eatery_profile',
            field=models.OneToOneField(to='eatery_profile.eatery_profile'),
        ),
    ]
