# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0002_upload_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='user',
        ),
        migrations.AlterField(
            model_name='upload',
            name='pic',
            field=models.FileField(upload_to='images/', verbose_name='Image'),
            preserve_default=True,
        ),
    ]
