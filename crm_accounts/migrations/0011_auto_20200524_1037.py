# Generated by Django 3.0.5 on 2020-05-24 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20200523_2132'),
        ('crm_accounts', '0010_auto_20200523_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimate',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.Clients'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.Clients'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estimate',
            name='estimate_id',
            field=models.CharField(default='R7XDg', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(default='hPFZk', max_length=10, unique=True),
        ),
    ]
