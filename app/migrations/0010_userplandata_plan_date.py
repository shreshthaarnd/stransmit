# Generated by Django 2.1.9 on 2020-07-21 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200721_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='userplandata',
            name='Plan_Date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
