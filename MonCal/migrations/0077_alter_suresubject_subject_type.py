# Generated by Django 3.2.23 on 2023-11-29 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0076_auto_20231129_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suresubject',
            name='subject_type',
            field=models.ManyToManyField(to='MonCal.Subject_type', verbose_name='設備区分'),
        ),
    ]
