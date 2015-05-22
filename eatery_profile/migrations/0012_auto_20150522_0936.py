# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0011_auto_20150522_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='food_hearts',
            field=models.ForeignKey(blank=True, to='eatery_profile.food_hearts', null=True),
        ),
        migrations.AlterField(
            model_name='specials',
            name='specials_hearts',
            field=models.ForeignKey(blank=True, to='eatery_profile.specials_hearts', null=True),
        ),
    ]
