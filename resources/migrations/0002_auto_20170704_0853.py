# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-04 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='resource',
            name='categories',
            field=models.ManyToManyField(to='resources.Category'),
        ),
    ]
