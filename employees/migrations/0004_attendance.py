# Generated by Django 3.0.5 on 2020-06-07 10:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_leaverequest_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendace', django.contrib.postgres.fields.jsonb.JSONField()),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employees.Staff')),
            ],
        ),
    ]
