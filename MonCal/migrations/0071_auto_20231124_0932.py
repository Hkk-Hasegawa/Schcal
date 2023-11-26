# Generated by Django 3.2.23 on 2023-11-24 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MonCal', '0070_auto_20231124_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='subject_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MonCal.subject_type', verbose_name='設備区分'),
        ),
        migrations.AlterField(
            model_name='eventschedule',
            name='updateuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AlterField(
            model_name='suresubject',
            name='subject_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MonCal.subject_type', verbose_name='設備区分'),
        ),
    ]
