# Generated by Django 3.0.5 on 2020-08-08 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0006_auto_20200808_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='attachement',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]