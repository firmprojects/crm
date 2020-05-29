# Generated by Django 3.0.5 on 2020-05-23 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0003_auto_20200523_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='add_team_member',
        ),
        migrations.AlterField(
            model_name='projects',
            name='add_project_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
