# Generated by Django 3.2.23 on 2023-11-16 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0042_alter_schedule_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateField(null=True, verbose_name='日付'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='endtime',
            field=models.TimeField(null=True, verbose_name='終了時刻'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='starttime',
            field=models.TimeField(null=True, verbose_name='開始時刻'),
        ),
    ]
