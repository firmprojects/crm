# Generated by Django 3.0.5 on 2020-06-07 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0028_auto_20200607_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='az2NY', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='fTT7R', max_length=10, unique=True),
        ),
    ]