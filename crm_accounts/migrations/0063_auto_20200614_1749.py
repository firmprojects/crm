# Generated by Django 3.0.5 on 2020-06-14 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0062_auto_20200614_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='WyBo2', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='WEB6d', max_length=10, unique=True),
        ),
    ]
