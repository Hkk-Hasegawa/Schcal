# Generated by Django 3.2.23 on 2023-11-08 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MonCal', '0011_auto_20231108_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
    ]
