# Generated by Django 4.0.1 on 2022-02-10 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20210722_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floormap',
            name='image',
            field=models.ImageField(upload_to='static/tracking/'),
        ),
    ]
