# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0007_item_itemid'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='picture',
            field=models.FileField(null=True, blank=True, upload_to='items/'),
            preserve_default=True,
        ),
    ]
