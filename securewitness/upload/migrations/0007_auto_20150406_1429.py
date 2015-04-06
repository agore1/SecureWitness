# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import upload.models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_auto_20150406_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_keyword',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('keyword', models.CharField(max_length=20)),
                ('report', models.ForeignKey(to='upload.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='report',
            name='short_desc',
            field=models.CharField(default='None', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report_file',
            name='file',
            field=models.FileField(upload_to=upload.models.file_path_maker),
            preserve_default=True,
        ),
    ]
