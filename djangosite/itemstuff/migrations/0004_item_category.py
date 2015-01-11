# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0003_item_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
