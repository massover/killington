# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 17:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0008_auto_20170321_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='SES',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ses_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
