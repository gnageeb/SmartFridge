# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-05 12:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartfridgeapp', '0008_auto_20170305_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item_fridge',
            old_name='fridge_id',
            new_name='fridge',
        ),
        migrations.RenameField(
            model_name='item_fridge',
            old_name='item_id',
            new_name='item',
        ),
    ]
