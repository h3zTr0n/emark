# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountstuff', '0006_auto_20150121_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='profile_picture',
            field=models.FileField(upload_to='media/', blank=True, null=True),
            preserve_default=True,
        ),
    ]
