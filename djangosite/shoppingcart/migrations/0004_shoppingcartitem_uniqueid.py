# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0003_auto_20150119_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcartitem',
            name='uniqueid',
            field=models.TextField(default='temp'),
            preserve_default=True,
        ),
    ]
