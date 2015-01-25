# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accountstuff', '0009_auto_20150125_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='followers',
            field=models.ManyToManyField(related_name='slaves', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
