# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0004_shoppingcartitem_uniqueid'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcartitem',
            name='pending',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shoppingcartitem',
            name='received',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
