# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0012_auto_20150522_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='food_hearts',
        ),
        migrations.AddField(
            model_name='food',
            name='food_hearts',
            field=models.ManyToManyField(to='eatery_profile.food_hearts', null=True, blank=True),
        ),
        migrations.RemoveField(
            model_name='specials',
            name='specials_hearts',
        ),
        migrations.AddField(
            model_name='specials',
            name='specials_hearts',
            field=models.ManyToManyField(to='eatery_profile.specials_hearts', null=True, blank=True),
        ),
    ]
