# Generated by Django 4.2.6 on 2023-11-19 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_unit_files_alter_unit_lectures_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='files',
            field=models.ManyToManyField(blank=True, to='main.file'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='lectures',
            field=models.ManyToManyField(blank=True, to='main.lecture'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='references',
            field=models.ManyToManyField(blank=True, to='main.reference'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='tasks',
            field=models.ManyToManyField(blank=True, to='main.task'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='tests',
            field=models.ManyToManyField(blank=True, to='main.test'),
        ),
    ]