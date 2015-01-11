# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0002_item_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
