# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-25 20:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_trackedposts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TrackedPosts',
            new_name='BookTracked',
        ),
    ]
