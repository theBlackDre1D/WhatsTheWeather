# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-23 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeatherApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='pressure',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='tempreature',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='wind',
            field=models.IntegerField(),
        ),
    ]