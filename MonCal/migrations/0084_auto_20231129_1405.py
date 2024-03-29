# Generated by Django 3.2.23 on 2023-11-29 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0083_auto_20231129_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventschedule',
            name='place',
            field=models.ManyToManyField(blank=True, to='MonCal.Event', verbose_name='場所'),
        ),
        migrations.AlterField(
            model_name='eventschedule',
            name='subject',
            field=models.ManyToManyField(blank=True, to='MonCal.Suresubject', verbose_name='利用設備'),
        ),
        migrations.AlterField(
            model_name='eventschedule',
            name='subschedule',
            field=models.ManyToManyField(blank=True, to='MonCal.Schedule', verbose_name='設備スケジュール'),
        ),
    ]
