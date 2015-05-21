# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eatery_profile', '0007_food_user_liked'),
    ]

    operations = [
        migrations.CreateModel(
            name='specials_hearts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_hearted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='specials',
            name='user_liked',
        ),
        migrations.AddField(
            model_name='specials_hearts',
            name='specials',
            field=models.ManyToManyField(to='eatery_profile.specials'),
        ),
        migrations.AddField(
            model_name='specials_hearts',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
