# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='special_tags',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='id',
        ),
        migrations.AlterField(
            model_name='special_tags',
            name='keyword',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='keyword',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
    ]
