# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-04 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20170704_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='categories',
            field=models.ManyToManyField(related_name='categories', to='resources.Category'),
        ),
    ]
