# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0005_specials_user_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specials',
            name='user_liked',
            field=models.BooleanField(default=False),
        ),
    ]
