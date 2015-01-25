# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountstuff', '0007_auto_20150122_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='profile_picture',
            field=models.FileField(null=True, blank=True, upload_to='users/'),
            preserve_default=True,
        ),
    ]
