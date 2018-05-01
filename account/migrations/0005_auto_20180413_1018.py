# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-13 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='item',
            name='item',
            field=models.CharField(choices=[('book', 'Book'), ('movie', 'Movie'), ('data', 'Data'), ('other', 'Other')], default='Data', max_length=10, verbose_name='Item Type'),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterIndexTogether(
            name='item',
            index_together=set([('id', 'slug')]),
        ),
    ]
