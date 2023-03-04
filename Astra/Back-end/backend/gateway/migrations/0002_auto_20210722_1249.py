# Generated by Django 3.1.5 on 2021-07-22 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mastergateway',
            old_name='macaddress',
            new_name='gatewayid',
        ),
        migrations.RenameField(
            model_name='slavegateway',
            old_name='macaddress',
            new_name='gatewayid',
        ),
        migrations.AddField(
            model_name='mastergateway',
            name='lastseen',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='slavegateway',
            name='lastseen',
            field=models.DateTimeField(auto_now=True),
        ),
    ]