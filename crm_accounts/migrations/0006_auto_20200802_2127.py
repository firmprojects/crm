# Generated by Django 3.0.6 on 2020-08-02 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0005_auto_20200802_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='xxogW', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='Hb7wL', max_length=10, unique=True),
        ),
    ]