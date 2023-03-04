# Generated by Django 3.1.5 on 2021-08-10 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20210722_1249'),
        ('sensor', '0003_dailytemperaturehumidity_monthlytemperaturehumidity_weeklytemperaturehumidity'),
    ]

    operations = [
        migrations.AddField(
            model_name='irq',
            name='co2',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='irq',
            name='floor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.floormap'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='irq',
            name='tvoc',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='irq',
            name='x',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='irq',
            name='y',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
