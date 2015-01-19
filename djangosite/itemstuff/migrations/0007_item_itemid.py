# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0006_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='itemid',
            field=models.TextField(default='tempid12345'),
            preserve_default=False,
        ),
    ]
