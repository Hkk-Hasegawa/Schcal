# Generated by Django 3.2.23 on 2023-11-17 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0048_remove_schedule_frame'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='member',
            field=models.ManyToManyField(blank=True, to='MonCal.Person', verbose_name='メンバー'),
        ),
    ]
