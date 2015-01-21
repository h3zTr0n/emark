# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountstuff', '0005_auto_20150111_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='/media/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='bio',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
