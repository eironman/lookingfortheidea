# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-12 22:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.PostComment'),
        ),
    ]