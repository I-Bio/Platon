# Generated by Django 4.2.6 on 2023-10-20 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_file_id_alter_lecture_id_alter_papa_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='study_Group',
            new_name='studyGroup',
        ),
    ]
