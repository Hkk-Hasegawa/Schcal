# Generated by Django 3.2.23 on 2023-12-25 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0107_eventschedule_swap_mode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventschedule',
            name='swap_mode',
        ),
    ]
