# Generated by Django 3.2.23 on 2023-11-23 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0067_alter_eventschedule_subject_pk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventschedule',
            name='subject_pk',
            field=models.PositiveBigIntegerField(default=0, verbose_name='利用設備'),
        ),
    ]
