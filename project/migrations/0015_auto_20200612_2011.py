# Generated by Django 3.0.5 on 2020-06-12 20:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_auto_20200612_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='file',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FileField(blank=True, null=True, upload_to=''), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='projects',
            name='image',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(blank=True, null=True, upload_to=''), default=list, size=None),
        ),
    ]
