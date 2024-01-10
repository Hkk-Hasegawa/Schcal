# Generated by Django 3.2.23 on 2023-11-20 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MonCal', '0050_remove_schedule_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excludeday',
            name='cycle',
        ),
        migrations.AddField(
            model_name='schedule',
            name='cycle',
            field=models.CharField(default='繰り返さない', max_length=15, verbose_name='繰り返し'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='member',
            field=models.ManyToManyField(blank=True, to='MonCal.Person', verbose_name='メンバー'),
        ),
        migrations.DeleteModel(
            name='Cycle',
        ),
        migrations.DeleteModel(
            name='Excludeday',
        ),
    ]
