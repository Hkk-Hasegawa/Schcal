# Generated by Django 3.2.23 on 2023-11-30 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0086_cycle_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventschedule',
            name='cycle_type',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='MonCal.cycle_type', verbose_name='繰り返し区分'),
        ),
    ]