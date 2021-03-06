# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 22:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('raw_data', models.CharField(max_length=100000)),
            ],
        ),
        migrations.CreateModel(
            name='UnitHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('status', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UnitInformation',
            fields=[
                ('name', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=10)),
                ('building', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=20)),
                ('price', models.CharField(max_length=10)),
                ('bedrooms', models.CharField(max_length=10)),
                ('floor', models.CharField(max_length=20)),
                ('area', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='unithistory',
            name='apartment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Deptford.UnitInformation'),
        ),
    ]
