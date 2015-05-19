# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0002_auto_20150519_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='specials',
            name='normal_price',
            field=models.DecimalField(default=1, max_digits=5, decimal_places=2),
            preserve_default=False,
        ),
    ]
