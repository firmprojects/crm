# Generated by Django 3.0.5 on 2020-08-25 23:36

import crm_accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('client_address', models.TextField()),
                ('billing_address', models.TextField()),
                ('extimate_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('amount', models.FloatField(blank=True, null=True)),
                ('estimate_id', models.CharField(default=crm_accounts.models.ran_gen, max_length=10, unique=True)),
                ('status', models.CharField(choices=[('accept', 'Accept'), ('reject', 'Reject'), ('pending', 'Pending')], max_length=100)),
                ('discount', models.FloatField(blank=True, default=0, max_length=100, null=True)),
                ('other_information', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200)),
                ('purchase_from', models.CharField(max_length=200)),
                ('purchase_date', models.DateField(blank=True)),
                ('purchase_by', models.CharField(max_length=200)),
                ('amount', models.FloatField()),
                ('paid_by', models.CharField(choices=[('cash', 'Cash'), ('transfer', 'Tranfer'), ('bank deposit', 'Bank Deposit'), ('cheque', 'Cheque'), ('others', 'Others')], max_length=20)),
                ('status', models.CharField(choices=[('inspect', 'Inspect'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=20)),
                ('attachement', models.FileField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='InoviceItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200, verbose_name='')),
                ('item_description', models.CharField(max_length=200, verbose_name='')),
                ('unit_cost', models.IntegerField(verbose_name='')),
                ('quantity', models.IntegerField(verbose_name='')),
                ('total', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('client_address', models.TextField()),
                ('billing_address', models.TextField()),
                ('invoice_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('invoice_id', models.CharField(default=crm_accounts.models.ran_gen, max_length=10, unique=True)),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('reject', 'Reject'), ('pending', 'Pending')], max_length=100)),
                ('discount', models.FloatField(blank=True, default=0, max_length=100, null=True)),
                ('other_information', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProvidentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Taxes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_name', models.CharField(max_length=100)),
                ('tax_percentage', models.FloatField()),
                ('tax_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200, verbose_name='')),
                ('item_description', models.CharField(max_length=200, verbose_name='')),
                ('unit_cost', models.IntegerField(verbose_name='')),
                ('quantity', models.IntegerField(verbose_name='')),
                ('total', models.IntegerField(default=0)),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_accounts.Estimate')),
            ],
        ),
    ]
