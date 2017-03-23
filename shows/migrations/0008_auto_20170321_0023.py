# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 00:23
from __future__ import unicode_literals

from django.db import migrations, models
import shows.utils


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0007_auto_20170308_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=shows.utils.generate_confirmation_code, max_length=32),
        ),
        migrations.AddField(
            model_name='user',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
