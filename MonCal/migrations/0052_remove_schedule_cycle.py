# Generated by Django 3.2.23 on 2023-11-20 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0051_auto_20231120_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='cycle',
        ),
    ]
