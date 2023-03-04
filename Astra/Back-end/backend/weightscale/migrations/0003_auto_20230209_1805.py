# Generated by Django 3.1.6 on 2023-02-09 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weightscale', '0002_auto_20221219_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagid', models.CharField(default=None, max_length=100)),
                ('baseValue', models.FloatField(default=0.0, null=True)),
                ('currentValue', models.FloatField(default=0.0, null=True)),
                ('previousValue', models.FloatField(default=0.0, null=True)),
                ('currentDiff', models.FloatField(default=0.0, null=True)),
                ('previousDiff', models.FloatField(default=0.0, null=True)),
                ('reading', models.FloatField(default=0.0, null=True)),
                ('distancelader', models.FloatField(default=0.0, null=True)),
                ('dcstatus', models.IntegerField(default=0, null=True)),
                ('battery', models.FloatField(default=0.0, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='SensorDaily',
        ),
        migrations.AlterField(
            model_name='sensorreading',
            name='tagid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='weightscale.sensors'),
        ),
    ]
