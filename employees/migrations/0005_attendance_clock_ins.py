# Generated by Django 3.0.5 on 2020-06-07 10:34

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='clock_ins',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]