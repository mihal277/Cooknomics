# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 16:10
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]