# Generated by Django 3.1.6 on 2023-02-10 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weightscale', '0003_auto_20230209_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensors',
            name='display',
            field=models.FloatField(default=0),
        ),
    ]