# Generated by Django 3.0.5 on 2020-06-08 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0033_auto_20200608_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='5c80J', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='6GFG6', max_length=10, unique=True),
        ),
    ]
