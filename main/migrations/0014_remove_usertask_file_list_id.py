# Generated by Django 4.2.6 on 2023-11-24 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_usertask_checker_grade_alter_usertask_grade_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertask',
            name='file_list_id',
        ),
    ]