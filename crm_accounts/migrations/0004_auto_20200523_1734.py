# Generated by Django 3.0.5 on 2020-05-23 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0003_auto_20200523_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='vrw2o', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='qTdJV', max_length=10, unique=True),
        ),
    ]
