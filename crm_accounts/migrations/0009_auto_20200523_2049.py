# Generated by Django 3.0.5 on 2020-05-23 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0008_auto_20200523_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='LEDQn', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='J5PXG', max_length=10, unique=True),
        ),
    ]
