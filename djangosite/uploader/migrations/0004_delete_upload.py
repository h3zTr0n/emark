# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0003_auto_20150122_0014'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Upload',
        ),
    ]