# Generated by Django 3.0.6 on 2020-08-01 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(default='default.jpg', upload_to='users'),
        ),
    ]