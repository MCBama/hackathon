# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Dead', 'Dead'), ('Critical', 'Critical'), ('Injured', 'Injured'), ('Ok', 'Ok')], default='Ok', max_length=20)),
            ],
        ),
    ]
