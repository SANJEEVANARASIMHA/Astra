# Generated by Django 4.0.1 on 2022-02-24 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_floormap_image'),
        ('alert', '0002_alter_alert_asset'),
        ('employee', '0007_auto_20210805_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeregistration',
            name='address',
        ),
        migrations.RemoveField(
            model_name='employeeregistration',
            name='email',
        ),
        migrations.RemoveField(
            model_name='employeeregistration',
            name='empid',
        ),
        migrations.RemoveField(
            model_name='employeeregistration',
            name='phoneno',
        ),
        migrations.AddField(
            model_name='employeeregistration',
            name='battery',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='employeeregistration',
            name='floor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.floormap'),
        ),
        migrations.AddField(
            model_name='employeeregistration',
            name='lastseen',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='employeeregistration',
            name='roll',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='employeeregistration',
            name='x',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='employeeregistration',
            name='y',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='employeeregistration',
            name='intime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='employeeregistration',
            name='tagid',
            field=models.CharField(default=None, max_length=20, unique=True),
        ),
        migrations.DeleteModel(
            name='EmployeeTag',
        ),
    ]