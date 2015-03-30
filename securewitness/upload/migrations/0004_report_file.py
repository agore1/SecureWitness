# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_auto_20150329_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='file',
            field=models.FileField(upload_to='', default='null'),
            preserve_default=True,
        ),
    ]
