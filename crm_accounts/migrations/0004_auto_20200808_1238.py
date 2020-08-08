# Generated by Django 3.0.5 on 2020-08-08 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0003_auto_20200807_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='paid_by',
            field=models.CharField(choices=[('ca', 'Cash'), ('tf', 'Tranfer'), ('bd', 'Bank Deposit'), ('ch', 'Cheque'), ('ot', 'Ot')], max_length=20),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='status',
            field=models.CharField(choices=[('Inspect', 'inspect'), ('Approved', 'approved'), ('Rejected', 'rejected')], max_length=20),
        ),
    ]