# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-24 00:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import downloadapp.storage
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', markdownx.models.MarkdownxField()),
                ('simple_description', models.CharField(max_length=300, null=True)),
                ('date_changed', models.DateTimeField(auto_now_add=True)),
                ('shot', models.ImageField(max_length=200, storage=downloadapp.storage.saveSmartFileShot(), upload_to='')),
                ('catagory', models.CharField(choices=[('GAM', 'Games'), ('APP', 'Apps'), ('DEV', 'Devloper tools'), ('MED', 'Media')], default='APP', max_length=3)),
                ('software', models.FileField(storage=downloadapp.storage.saveSmartFileSoft(), upload_to='')),
                ('installs', models.IntegerField(default=2)),
                ('stage', models.CharField(choices=[('LOK', 'Certification'), ('LIV', 'Live!')], default='LOK', max_length=3)),
                ('message', models.TextField(null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
