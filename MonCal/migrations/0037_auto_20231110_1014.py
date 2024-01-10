# Generated by Django 3.2.23 on 2023-11-10 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0036_alter_schedule_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='endtime',
            field=models.TimeField(blank=True, null=True, verbose_name='終了時刻'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='starttime',
            field=models.TimeField(blank=True, null=True, verbose_name='開始時刻'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(null=True),
        ),
    ]
