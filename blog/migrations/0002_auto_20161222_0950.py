# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-22 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmedia',
            name='order',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]