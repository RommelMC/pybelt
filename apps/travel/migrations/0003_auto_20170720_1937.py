# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-20 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20170720_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='endDate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='startDate',
            field=models.DateTimeField(),
        ),
    ]
