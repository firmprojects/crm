# Generated by Django 3.0.5 on 2020-08-18 15:17

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('is_client', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=False)),
                ('joined', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(default='users/doc_avatar.jpg', upload_to='users')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('assigned_to', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('asset_name', models.CharField(max_length=100)),
                ('asset_id', models.CharField(blank=True, default=users.models.generate_asset_id, max_length=10, unique=True)),
                ('purchase_date', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('assigned_date', models.DateField(blank=True)),
                ('warranty_end', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('asset_amount', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('approved', 'Approved'), ('inspect', 'Inspect'), ('missing', 'Missing'), ('rejected', 'Rejected')], max_length=50)),
                ('receipt', models.FileField(blank=True, upload_to='receipts')),
            ],
        ),
        migrations.CreateModel(
            name='Clocking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clockin_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
