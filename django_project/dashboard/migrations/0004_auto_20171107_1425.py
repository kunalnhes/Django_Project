# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20171107_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=120)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
