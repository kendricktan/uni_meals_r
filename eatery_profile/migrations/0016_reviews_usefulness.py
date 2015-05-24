# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eatery_profile', '0015_auto_20150522_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='reviews_usefulness',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_useful', models.BooleanField()),
                ('reviews', models.ForeignKey(to='eatery_profile.reviews')),
                ('user_profile', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
