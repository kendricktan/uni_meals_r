# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import user_profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='picture',
            field=models.ImageField(null=True, upload_to=user_profile.models.generate_directory_user, blank=True),
        ),
    ]
