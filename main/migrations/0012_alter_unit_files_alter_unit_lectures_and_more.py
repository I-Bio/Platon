# Generated by Django 4.2.6 on 2023-11-19 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_task_subject_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='files',
            field=models.ManyToManyField(null=True, to='main.file'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='lectures',
            field=models.ManyToManyField(null=True, to='main.lecture'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='references',
            field=models.ManyToManyField(null=True, to='main.reference'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='tasks',
            field=models.ManyToManyField(null=True, to='main.task'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='tests',
            field=models.ManyToManyField(null=True, to='main.test'),
        ),
    ]