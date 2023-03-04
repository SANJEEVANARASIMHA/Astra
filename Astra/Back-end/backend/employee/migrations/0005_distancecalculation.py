# Generated by Django 3.1.5 on 2021-07-29 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_distancetracking'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistanceCalculation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empid', models.IntegerField()),
                ('name1', models.CharField(max_length=100)),
                ('name2', models.CharField(max_length=100)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('duration', models.CharField(max_length=50)),
            ],
        ),
    ]