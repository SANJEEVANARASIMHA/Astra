# Generated by Django 3.1.6 on 2022-12-19 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy', '0004_alter_energytracking_powerfactor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='energytracking',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='passiveasset',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vehicletracking',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]