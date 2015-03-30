# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='author',
            field=models.CharField(default='Anonymous', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='title',
            field=models.CharField(default='Untitled', max_length=200),
            preserve_default=True,
        ),
    ]
