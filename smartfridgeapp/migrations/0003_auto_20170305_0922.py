# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-05 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartfridgeapp', '0002_auto_20170305_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fridge_day_calories',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
