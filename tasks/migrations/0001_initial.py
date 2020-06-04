# Generated by Django 3.0.5 on 2020-06-03 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0007_auto_20200529_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('priority', models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], max_length=50)),
                ('status', models.CharField(choices=[('working', 'Working'), ('pending', 'Pending'), ('suspended', 'Suspended'), ('cancelled', 'cancelled')], max_length=50)),
                ('description', models.TextField()),
                ('files', models.FileField(blank=True, null=True, upload_to='')),
                ('assign_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_asignee', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
                ('task_followers', models.ManyToManyField(blank=True, related_name='task_followers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticketing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateField(blank=True, null=True)),
                ('total_hours', models.IntegerField(default=0)),
                ('remaining_hours', models.IntegerField(default=0)),
                ('date', models.DateField(blank=True, null=True)),
                ('hours', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
            ],
        ),
        migrations.CreateModel(
            name='TaskTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('task_duration', models.CharField(blank=True, max_length=200, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task')),
            ],
        ),
    ]
