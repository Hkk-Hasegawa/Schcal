# Generated by Django 3.2.23 on 2023-11-07 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0006_auto_20231107_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calsetting',
            name='Step',
            field=models.PositiveSmallIntegerField(verbose_name='刻み幅（分）'),
        ),
    ]
