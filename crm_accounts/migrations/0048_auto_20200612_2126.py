# Generated by Django 3.0.5 on 2020-06-12 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0047_auto_20200612_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='E3OYS', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='oq2MH', max_length=10, unique=True),
        ),
    ]
