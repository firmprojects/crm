# Generated by Django 3.0.5 on 2020-06-12 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0042_auto_20200612_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='dIL8A', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='nQuNh', max_length=10, unique=True),
        ),
    ]
