# Generated by Django 3.0.3 on 2020-02-25 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='srtmodel',
            name='srt',
            field=models.FileField(upload_to='srts/'),
        ),
        migrations.AlterField(
            model_name='videomodel',
            name='video',
            field=models.FileField(upload_to='videos/'),
        ),
    ]
