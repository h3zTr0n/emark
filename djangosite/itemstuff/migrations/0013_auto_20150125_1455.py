# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0012_auto_20150125_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='averagerating',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
