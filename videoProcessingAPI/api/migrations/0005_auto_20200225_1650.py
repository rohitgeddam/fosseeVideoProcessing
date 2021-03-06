# Generated by Django 3.0.3 on 2020-02-25 16:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_chunk_fusedresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chunk',
            name='timeInHours',
        ),
        migrations.RemoveField(
            model_name='chunk',
            name='timeInMilliSeconds',
        ),
        migrations.RemoveField(
            model_name='chunk',
            name='timeInMinutes',
        ),
        migrations.RemoveField(
            model_name='chunk',
            name='timeInSeconds',
        ),
        migrations.AddField(
            model_name='chunk',
            name='startTime',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
