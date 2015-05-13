# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models_functions


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150513_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='eatery',
            name='picture',
            field=models.ImageField(null=True, upload_to=main.models_functions.generate_directory_eatery, blank=True),
        ),
        migrations.AddField(
            model_name='specials',
            name='picture',
            field=models.ImageField(null=True, upload_to=main.models_functions.generate_directory_specials, blank=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='picture',
            field=models.ImageField(null=True, upload_to=main.models_functions.generate_directory_food, blank=True),
        ),
    ]
