# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-04 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0002_auto_20171204_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]