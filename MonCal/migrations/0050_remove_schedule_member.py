# Generated by Django 3.2.23 on 2023-11-20 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0049_alter_schedule_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='member',
        ),
    ]
