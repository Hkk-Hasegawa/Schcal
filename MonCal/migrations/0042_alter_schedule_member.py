# Generated by Django 3.2.23 on 2023-11-13 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0041_alter_schedule_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='member',
            field=models.ManyToManyField(blank=True, to='MonCal.Person', verbose_name='メンバー'),
        ),
    ]
