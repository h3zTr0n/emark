# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 10, 22, 57, 27, 699123, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
