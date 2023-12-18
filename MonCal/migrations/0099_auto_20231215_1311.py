# Generated by Django 3.2.23 on 2023-12-15 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0098_schedule_cycle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suresubject',
            name='name',
            field=models.CharField(max_length=31, verbose_name='社用車'),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, verbose_name='部屋名')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MonCal.pause_type', verbose_name='場所')),
            ],
        ),
    ]