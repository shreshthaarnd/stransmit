# Generated by Django 2.1.9 on 2020-07-21 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_userplandata_plan_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userplandata',
            name='Plan_Date',
            field=models.DateField(auto_now=True),
        ),
    ]
