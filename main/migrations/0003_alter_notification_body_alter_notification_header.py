# Generated by Django 4.2.6 on 2023-11-18 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_notification_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='body',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='notification',
            name='header',
            field=models.CharField(max_length=40),
        ),
    ]
