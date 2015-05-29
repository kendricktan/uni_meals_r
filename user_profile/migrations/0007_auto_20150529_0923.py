# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_auto_20150522_0932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message_reply',
            name='message',
        ),
        migrations.RemoveField(
            model_name='message',
            name='op_id',
        ),
        migrations.RemoveField(
            model_name='message',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='message',
            name='op_user_profile',
            field=models.ForeignKey(related_name='op_user_profile', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='original_message',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='received_user_profile',
            field=models.ForeignKey(related_name='received_user_profile', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.DeleteModel(
            name='message_reply',
        ),
    ]
