# Generated by Django 4.2.6 on 2023-11-16 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_rename_groups_name_subject_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='user_id',
            new_name='users_id',
        ),
    ]
