# Generated by Django 3.0.5 on 2020-08-04 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounts', '0007_auto_20200803_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='AvjtOP', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='attachement',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='paid_by',
            field=models.CharField(blank=True, choices=[('ca', 'Cash'), ('tf', 'Tranfer'), ('bd', 'Bank Deposit'), ('ch', 'Cheque'), ('ot', 'Ot')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='purchase_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='status',
            field=models.CharField(blank=True, choices=[('pd', 'Pending'), ('ap', 'Approved')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='ycMF2A', max_length=10, unique=True),
        ),
    ]