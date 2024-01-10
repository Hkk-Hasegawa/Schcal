# Generated by Django 3.2.23 on 2023-11-28 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0073_auto_20231124_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='Working_days',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('weekend_f', models.BooleanField(null=True, verbose_name='土日判定')),
            ],
        ),
    ]
