# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 19:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={},
        ),
        migrations.RemoveField(
            model_name='lottery',
            name='lottery_id',
        ),
        migrations.AddField(
            model_name='lottery',
            name='ends_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lottery',
            name='external_performance_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lottery',
            name='entered_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lottery',
            name='nonce',
            field=models.CharField(blank=True, max_length=31, null=True),
        ),
        migrations.AlterField(
            model_name='lottery',
            name='starts_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='subscribed_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(verbose_name='date of birth'),
        ),
    ]
