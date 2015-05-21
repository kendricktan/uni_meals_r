# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0008_auto_20150521_0918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specials_hearts',
            name='specials',
        ),
        migrations.AddField(
            model_name='specials',
            name='specials_hearts',
            field=models.ManyToManyField(to='eatery_profile.specials_hearts'),
        ),
    ]
