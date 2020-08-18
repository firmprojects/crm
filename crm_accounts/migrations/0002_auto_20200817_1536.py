# Generated by Django 3.0.5 on 2020-08-17 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
        ('crm_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='providentfund',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='items',
            name='estimate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_accounts.Estimate'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Clients'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='projects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='taxes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_accounts.Taxes'),
        ),
        migrations.AddField(
            model_name='estimate',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Clients'),
        ),
        migrations.AddField(
            model_name='estimate',
            name='projects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects'),
        ),
        migrations.AddField(
            model_name='estimate',
            name='taxes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_accounts.Taxes'),
        ),
    ]