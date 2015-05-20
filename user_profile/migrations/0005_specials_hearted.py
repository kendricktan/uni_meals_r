# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_remove_eatery_reviewed_review_stars'),
    ]

    operations = [
        migrations.CreateModel(
            name='specials_hearted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('specials_id', models.IntegerField()),
                ('datetime_hearted', models.DateTimeField(auto_now_add=True)),
                ('timeline', models.ForeignKey(to='user_profile.timeline')),
            ],
        ),
    ]
