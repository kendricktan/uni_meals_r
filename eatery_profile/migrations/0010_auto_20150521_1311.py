# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eatery_profile', '0009_auto_20150521_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='food_hearts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_hearted', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='food',
            name='user_liked',
        ),
        migrations.AlterField(
            model_name='specials',
            name='specials_hearts',
            field=models.ManyToManyField(to='eatery_profile.specials_hearts', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='food',
            name='food_hearts',
            field=models.ManyToManyField(to='eatery_profile.food_hearts', null=True, blank=True),
        ),
    ]
