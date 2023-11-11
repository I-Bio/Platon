# Generated by Django 4.2.6 on 2023-11-10 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_task_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentfile',
            name='name',
        ),
        migrations.AddField(
            model_name='studentfile',
            name='creator',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentfile',
            name='task_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
