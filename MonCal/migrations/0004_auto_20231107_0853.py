# Generated by Django 3.2.23 on 2023-11-06 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0003_rename_subject_suresubject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='date',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='usetime',
        ),
        migrations.AddField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='終了時間'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='開始時間'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='subject_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MonCal.suresubject', verbose_name='予約対象'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='user',
            field=models.CharField(max_length=255, verbose_name='予約者名'),
        ),
    ]
