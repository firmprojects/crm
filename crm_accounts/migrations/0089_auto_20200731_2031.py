# Generated by Django 3.0.6 on 2020-07-31 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0088_auto_20200731_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='WVqwd', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='fNnFv', max_length=10, unique=True),
        ),
    ]
