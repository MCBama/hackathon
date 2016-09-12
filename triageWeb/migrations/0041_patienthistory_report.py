# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-09 21:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('triageWeb', '0040_disease_disease_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='triageWeb.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=30, default=0.0, max_digits=50)),
                ('longitude', models.DecimalField(decimal_places=30, default=0.0, max_digits=50)),
                ('report_time', models.DateTimeField(auto_now_add=True)),
                ('center', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='triageWeb.HealthCenter')),
                ('patient_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triageWeb.PatientHistory')),
                ('reporter', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='triageWeb.Reporter')),
            ],
        ),
    ]
