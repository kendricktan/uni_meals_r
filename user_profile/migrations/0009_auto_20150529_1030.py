# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0008_message_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
