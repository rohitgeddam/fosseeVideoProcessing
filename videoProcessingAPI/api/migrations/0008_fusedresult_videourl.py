# Generated by Django 3.0.3 on 2020-02-26 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200225_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='fusedresult',
            name='videoUrl',
            field=models.CharField(default='/media/downloadable/', max_length=500),
        ),
    ]
