# Generated by Django 4.2.6 on 2023-10-28 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_remove_usertask_first_name_remove_usertask_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertask',
            name='first_name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='usertask',
            name='last_name',
            field=models.CharField(max_length=256, null=True),
        ),
    ]