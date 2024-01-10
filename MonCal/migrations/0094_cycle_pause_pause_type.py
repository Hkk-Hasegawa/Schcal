# Generated by Django 3.2.23 on 2023-12-04 04:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MonCal', '0093_remove_schedule_subschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pause_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=31, verbose_name='コード')),
                ('name', models.CharField(max_length=31, verbose_name='名前')),
            ],
        ),
        migrations.CreateModel(
            name='Cycle_pause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='日付')),
                ('pause_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='MonCal.pause_type', verbose_name='繰り返し区分')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MonCal.eventschedule', verbose_name='行事予定')),
                ('updateuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]
