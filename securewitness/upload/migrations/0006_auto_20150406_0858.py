# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_remove_report_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='title',
        ),
        migrations.AddField(
            model_name='report',
            name='location',
            field=models.CharField(max_length=50, default='None'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='long_desc',
            field=models.CharField(max_length=500, default='None'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='short_desc',
            field=models.CharField(max_length=100, default='None'),
            preserve_default=True,
        ),
    ]
