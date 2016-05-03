# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('triageWeb', '0018_auto_20160503_0138'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriageArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TriageCoord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(decimal_places=13, default=0.0, max_digits=50)),
                ('lng', models.DecimalField(decimal_places=13, default=0.0, max_digits=50)),
            ],
        ),
        migrations.CreateModel(
            name='TriageGeometry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo_type', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TriageProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=20)),
                ('mapText', models.CharField(default='', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('green', models.IntegerField()),
                ('yellow', models.IntegerField()),
                ('red', models.IntegerField()),
                ('casualties', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='triagecoord',
            name='geoObj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triageWeb.TriageGeometry'),
        ),
        migrations.AddField(
            model_name='triagearea',
            name='geometry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triageWeb.TriageGeometry'),
        ),
        migrations.AddField(
            model_name='triagearea',
            name='properties',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triageWeb.TriageProperties'),
        ),
    ]
