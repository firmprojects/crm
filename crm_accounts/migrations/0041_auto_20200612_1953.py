# Generated by Django 3.0.5 on 2020-06-12 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0040_auto_20200612_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='f0MHx', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='mEVcy', max_length=10, unique=True),
        ),
    ]
