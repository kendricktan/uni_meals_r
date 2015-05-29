# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0009_auto_20150529_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='message_reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=32767)),
                ('datetime_sent', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='original_message',
        ),
        migrations.AddField(
            model_name='message_reply',
            name='message',
            field=models.ForeignKey(to='user_profile.message'),
        ),
        migrations.AddField(
            model_name='message_reply',
            name='op_user_profile',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
