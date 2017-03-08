# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 01:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import shows.managers


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0006_auto_20170302_2229'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', shows.managers.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='show',
            name='subscribed_users',
            field=models.ManyToManyField(blank=True, related_name='subscribed_shows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
