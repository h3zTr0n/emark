# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemstuff', '0011_auto_20150125_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='totalrating',
            new_name='averagerating',
        ),
    ]
