# Generated by Django 3.0.5 on 2020-06-12 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_auto_20200612_2123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='file',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='image',
        ),
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
            ],
        ),
    ]