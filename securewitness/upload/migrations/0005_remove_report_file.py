# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_report_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='file',
        ),
    ]
