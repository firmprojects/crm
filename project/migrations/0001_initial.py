# Generated by Django 3.0.5 on 2020-07-22 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import project.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=20)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('photo', models.ImageField(default='default.jpg', upload_to='clients_pics')),
                ('clients_id', models.CharField(default=project.models.generate_client_id, max_length=20, unique=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('project_cost', models.PositiveIntegerField()),
                ('priority', models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], max_length=50)),
                ('status', models.CharField(choices=[('working', 'Working'), ('pending', 'Pending'), ('suspended', 'Suspended'), ('cancelled', 'cancelled')], max_length=50)),
                ('description', models.TextField()),
                ('project_id', models.CharField(default=project.models.generate_project_id, max_length=10, unique=True)),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Clients')),
                ('project_leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leader_set', to=settings.AUTH_USER_MODEL)),
                ('team_member', models.ManyToManyField(blank=True, related_name='team_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=200)),
                ('completed', models.BooleanField(default=False)),
                ('milestone_assignes', models.ManyToManyField(related_name='milestone_assignes', to=settings.AUTH_USER_MODEL)),
                ('milestone_followers', models.ManyToManyField(related_name='milestone_followers', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
            ],
        ),
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='images/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
            ],
        ),
        migrations.CreateModel(
            name='DocUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.FileField(blank=True, null=True, upload_to='document/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('commented_on', models.DateTimeField(auto_now_add=True)),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
            ],
        ),
    ]
