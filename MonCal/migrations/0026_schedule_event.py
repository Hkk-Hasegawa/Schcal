# Generated by Django 3.2.23 on 2023-11-08 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0025_alter_event_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='event',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='MonCal.event', verbose_name='イベント'),
        ),
    ]
