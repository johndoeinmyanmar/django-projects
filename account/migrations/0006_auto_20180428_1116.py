# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-28 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180413_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='cover',
            field=models.ImageField(blank=True, upload_to='items/%Y/%m/%d'),
        ),
    ]