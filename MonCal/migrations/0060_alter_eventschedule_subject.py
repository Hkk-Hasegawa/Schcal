# Generated by Django 3.2.23 on 2023-11-22 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0059_auto_20231122_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventschedule',
            name='subject',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='利用設備'),
        ),
    ]