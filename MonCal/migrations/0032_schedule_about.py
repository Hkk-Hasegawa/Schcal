# Generated by Django 3.2.23 on 2023-11-09 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0031_delete_calsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='詳細'),
        ),
    ]
