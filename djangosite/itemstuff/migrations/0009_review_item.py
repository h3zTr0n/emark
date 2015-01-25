# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0008_item_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='item',
            field=models.ForeignKey(to='itemstuff.Item', default=0),
            preserve_default=True,
        ),
    ]
