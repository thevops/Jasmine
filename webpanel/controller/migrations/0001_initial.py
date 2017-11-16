# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 20:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=64, unique=True)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DNS_Name', models.CharField(db_index=True, max_length=64, unique=True)),
                ('IP_Address', models.GenericIPAddressField(protocol='IPv4')),
                ('Description', models.TextField()),
                ('Last_Seen', models.DateTimeField()),
                ('Synchronization_Period', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=64, unique=True)),
                ('Description', models.TextField()),
                ('Configuration', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=64, unique=True)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(db_index=True, max_length=64, unique=True)),
                ('Description', models.TextField()),
                ('Module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controller.Modules')),
                ('Worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controller.Hosts')),
            ],
        ),
        migrations.AddField(
            model_name='hosts',
            name='Status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controller.Statuses'),
        ),
        migrations.AddField(
            model_name='groupassignment',
            name='Group_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controller.Groups'),
        ),
        migrations.AddField(
            model_name='groupassignment',
            name='Host_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controller.Hosts'),
        ),
    ]
