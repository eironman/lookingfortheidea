# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitorsbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorbookmessage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='visitorsbook/%Y/%m/%d/'),
        ),
    ]
