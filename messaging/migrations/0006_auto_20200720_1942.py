# Generated by Django 3.0.6 on 2020-07-20 19:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0005_auto_20200720_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailbody',
            name='files',
        ),
        migrations.AddField(
            model_name='mailbody',
            name='files',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to='document/'), blank=True, null=True, size=None),
        ),
        migrations.DeleteModel(
            name='Files',
        ),
    ]