# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0002_auto_20150119_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcartitem',
            name='item',
            field=models.ForeignKey(to='itemstuff.Item'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shoppingcartitem',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
