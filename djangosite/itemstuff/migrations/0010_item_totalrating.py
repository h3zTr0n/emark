# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0009_review_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='totalrating',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
