# Generated by Django 3.2.23 on 2023-11-21 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0056_schedule_cycle'),
    ]

    operations = [
        migrations.AddField(
            model_name='suresubject',
            name='subjectclass',
            field=models.CharField(max_length=31, null=True, verbose_name='区分'),
        ),
    ]