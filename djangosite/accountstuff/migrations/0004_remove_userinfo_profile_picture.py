# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountstuff', '0003_auto_20141227_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='profile_picture',
        ),
    ]
