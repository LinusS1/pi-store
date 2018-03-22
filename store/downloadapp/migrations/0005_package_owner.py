# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-19 03:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('downloadapp', '0004_remove_package_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
