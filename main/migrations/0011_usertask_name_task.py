# Generated by Django 4.2.6 on 2023-11-23 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_usertask_group_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertask',
            name='name_task',
            field=models.CharField(max_length=265, null=True),
        ),
    ]