# Generated by Django 3.2.23 on 2023-12-01 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0091_auto_20231201_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventschedule',
            name='place',
            field=models.ManyToManyField(to='MonCal.Event', verbose_name='場所'),
        ),
    ]
