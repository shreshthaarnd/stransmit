# Generated by Django 2.1.9 on 2020-07-29 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_maildata_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='maildata',
            name='key1',
            field=models.CharField(default='NA', max_length=100),
        ),
    ]
