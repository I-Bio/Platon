# Generated by Django 4.2.6 on 2023-12-15 18:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_notification_time_delivery_alter_task_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='time_delivery',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 18, 23, 30, 824794, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 18, 23, 30, 818810, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 18, 23, 30, 793877, tzinfo=datetime.timezone.utc)),
        ),
    ]
