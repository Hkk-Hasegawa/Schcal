# Generated by Django 3.2.23 on 2023-11-03 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('cal_url', models.TextField()),
            ],
        ),
    ]
