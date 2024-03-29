# Generated by Django 3.2.23 on 2023-11-08 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0008_alter_calsetting_subject_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='frame',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='コマ数'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='user',
            field=models.CharField(max_length=31, verbose_name='予約者名'),
        ),
        migrations.AlterField(
            model_name='suresubject',
            name='name',
            field=models.CharField(max_length=31, verbose_name='対象名'),
        ),
    ]
