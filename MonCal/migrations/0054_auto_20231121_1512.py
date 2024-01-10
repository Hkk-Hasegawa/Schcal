# Generated by Django 3.2.23 on 2023-11-21 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MonCal', '0053_schedule_cycle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, verbose_name='行事区分')),
                ('head_time', models.TimeField(null=True, verbose_name='受付開始時間')),
                ('tail_time', models.TimeField(null=True, verbose_name='受付終了時間')),
            ],
        ),
        migrations.CreateModel(
            name='weekday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ja_name', models.CharField(max_length=31, null=True, verbose_name='名前')),
                ('weeklynum', models.SmallIntegerField(default=0, verbose_name='コード上の数値')),
            ],
        ),
        migrations.RemoveField(
            model_name='suresubject',
            name='Step',
        ),
        migrations.RemoveField(
            model_name='suresubject',
            name='display_period',
        ),
        migrations.CreateModel(
            name='EventSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='日付')),
                ('starttime', models.TimeField(blank=True, null=True, verbose_name='開始時刻')),
                ('endtime', models.TimeField(blank=True, null=True, verbose_name='終了時刻')),
                ('title', models.CharField(max_length=31, null=True, verbose_name='タイトル')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='詳細')),
                ('cycle', models.CharField(default='nocycle', max_length=15, verbose_name='繰り返し')),
                ('Event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MonCal.event', verbose_name='予約対象')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MonCal.suresubject', verbose_name='予約対象')),
                ('updateuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]
