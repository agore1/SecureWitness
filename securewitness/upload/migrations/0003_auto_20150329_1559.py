# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20150325_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_field',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('txt', models.CharField(max_length=200)),
                ('ans', models.CharField(max_length=200)),
                ('report', models.ForeignKey(to='upload.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report_file',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('file', models.FileField(upload_to='')),
                ('report', models.ForeignKey(to='upload.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='form_field',
            name='report',
        ),
        migrations.DeleteModel(
            name='Form_field',
        ),
    ]
