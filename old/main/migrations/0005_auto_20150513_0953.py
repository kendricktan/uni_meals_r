# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models_functions


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_user_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eatery',
            name='absolute_coordinates',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='eatery',
            name='address',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='eatery',
            name='gmaps_url',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='eatery',
            name='pricing',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(null=True, upload_to=main.models_functions.generate_directory_user, blank=True),
        ),
    ]
