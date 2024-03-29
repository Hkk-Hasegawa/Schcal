# Generated by Django 3.2.23 on 2023-11-07 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0005_auto_20231107_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calsetting',
            name='Step',
            field=models.TimeField(verbose_name='刻み幅'),
        ),
        migrations.AlterField(
            model_name='calsetting',
            name='head_time',
            field=models.TimeField(verbose_name='受付開始時間'),
        ),
        migrations.AlterField(
            model_name='calsetting',
            name='tail_time',
            field=models.TimeField(verbose_name='受付終了時間'),
        ),
    ]
