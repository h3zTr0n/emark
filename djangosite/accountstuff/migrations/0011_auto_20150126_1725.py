# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accountstuff', '0010_auto_20150125_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='followers',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='slaves'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='following',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='masters'),
            preserve_default=True,
        ),
    ]
