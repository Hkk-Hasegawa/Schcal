# Generated by Django 3.2.23 on 2023-11-29 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0081_remove_suresubject_subjectclass'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventschedule',
            old_name='subject_pk',
            new_name='subject',
        ),
        migrations.RemoveField(
            model_name='event',
            name='subject_type',
        ),
    ]
