# Generated by Django 3.2.23 on 2023-11-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0018_delete_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=31, null=True, verbose_name='使用目的')),
            ],
        ),
    ]
