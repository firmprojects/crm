# Generated by Django 3.0.5 on 2020-05-23 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0005_auto_20200523_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='add_project_leader',
        ),
        migrations.AddField(
            model_name='projects',
            name='project_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leader_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projects',
            name='team_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_set', to=settings.AUTH_USER_MODEL),
        ),
    ]