# Generated by Django 2.1.9 on 2020-07-08 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200707_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='maildata',
            name='Subject',
            field=models.CharField(default='no-subject', max_length=200),
        ),
        migrations.AlterField(
            model_name='maildata',
            name='Mail_Date',
            field=models.CharField(default=datetime.date(2020, 7, 9), max_length=15),
        ),
        migrations.AlterField(
            model_name='sentdata',
            name='Mail_Date',
            field=models.CharField(default=datetime.date(2020, 7, 9), max_length=15),
        ),
    ]
