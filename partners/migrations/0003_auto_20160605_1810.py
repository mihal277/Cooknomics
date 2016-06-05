# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-05 18:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0002_auto_20160604_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to='partners/'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='url',
            field=models.CharField(blank=True, default=datetime.datetime(2016, 6, 5, 18, 10, 6, 759301, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
    ]
