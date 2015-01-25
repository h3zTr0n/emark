# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0010_item_totalrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='totalrating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
