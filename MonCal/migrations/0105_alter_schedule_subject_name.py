# Generated by Django 3.2.23 on 2023-12-15 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0104_eventschedule_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='subject_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MonCal.suresubject', verbose_name='予約対象'),
        ),
    ]
