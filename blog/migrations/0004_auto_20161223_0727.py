# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-23 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.CharField(blank=True, default=None, max_length=200),
        ),
    ]